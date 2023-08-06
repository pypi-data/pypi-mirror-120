#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Daemon component capable of converting IDEA (https://idea.cesnet.cz/) messages to MISP core format
(https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/) and inserting them to MISP instance.

The implementation is based on :py:class:`pyzenkit.zendaemon.ZenDaemonComponent`.
"""

import json
from typing import Tuple, Set, List, Optional
from uuid import uuid5, uuid4, UUID
from logging import getLogger

from pymisp import ExpandedPyMISP, MISPEvent, MISPObject, MISPOrganisation

import pyzenkit.zendaemon
import mentat.idea.internal

CONFIG_MISP_URL = "misp_url"
CONFIG_MISP_KEY = "misp_key"
CONFIG_MISP_CERT = "misp_cert"


class MisperDaemonComponent(pyzenkit.zendaemon.ZenDaemonComponent):
    """
    Daemon component capable of converting IDEA (https://idea.cesnet.cz/) messages to MISP core format
    (https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/) and inserting them to MISP instance.
    """
    EVENT_START = 'start'
    EVENT_STOP = 'stop'

    EVENT_MSG_PROCESS = 'message_process'
    EVENT_LOG_STATISTICS = 'log_statistics'

    STATS_CNT_CONVERTED = 'cnt_converted'
    STATS_CNT_ERRORS = 'cnt_errors'
    STATS_CNT_PUSHED = 'cnt_success_pushed'

    def __init__(self, **kwargs):
        """
        Perform component initializations.
        """
        super().__init__(**kwargs)

        # Unique component identifier
        self.cid = kwargs.get('cid', 'misper')

        self.misp_inst = None
        # TODO remove, just for debug purposes
        self.daemon = None

    def setup(self, daemon):
        """
        Perform component setup.
        """
        misp_key = daemon.c(CONFIG_MISP_KEY)
        misp_url = daemon.c(CONFIG_MISP_URL)
        misp_cert = daemon.c(CONFIG_MISP_CERT)

        daemon.logger.debug(f"Loaded arguments: key: {misp_key.replace(misp_key[5:-5], '*'*len(misp_key[5:-5]))},"
                            f" url: {misp_url}, cert: {misp_cert}!")
        self.misp_inst = ExpandedPyMISP(misp_url, misp_key, False if misp_cert == "" else misp_cert)

    def get_events(self):
        """
        Get the list of event names and their appropriate callback handlers.
        """
        return [
            {
                'event': self.EVENT_START,
                'callback': self.cbk_event_start,
                'prepend': False
            },
            {
                'event': self.EVENT_STOP,
                'callback': self.cbk_event_stop,
                'prepend': False
            },
            {
                'event': self.EVENT_MSG_PROCESS,
                'callback': self.cbk_event_message_process,
                'prepend': False
            },
            {
                'event': self.EVENT_LOG_STATISTICS,
                'callback': self.cbk_event_log_statistics,
                'prepend': False
            }
        ]

    # ---------------------------------------------------------------------------

    def cbk_event_start(self, daemon, args):
        """
        Start the component.
        """
        daemon.logger.debug(f"Component '{self.cid}': Starting the component")
        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_stop(self, daemon, args):
        """
        Stop the component.
        """
        daemon.logger.debug(f"Component '{self.cid}': Stopping the component")
        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_message_process(self, daemon, args):
        """
        Store the message into the persistent storage.
        """
        self.daemon = daemon
        # convert to raw json, without datetimes - for now, later can be updated
        daemon.logger.info(f"Received new idea event (uuid: {args['idea'].get_id()})!")
        daemon.logger.debug(f"Idea event: {args['idea']}")

        uuid_generator = UuidGenerator(idea_event=args['idea'], logger=daemon.logger)
        idea_to_misp_processor = IdeaToMispProcessor(daemon.logger, self.misp_inst, uuid_generator)
        idea_to_misp_processor.process_idea_event(args['idea'])

        self.daemon = None
        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_log_statistics(self, daemon, args):
        """
        Periodical processing statistics logging.
        """
        stats = self.get_statistics()
        stats_str = ''

        for k in [self.STATS_CNT_CONVERTED, self.STATS_CNT_PUSHED, self.STATS_CNT_ERRORS]:
            if k in stats:
                stats_str = self.pattern_stats.format(stats_str, k, stats[k]['cnt'], stats[k]['inc'], stats[k]['spd'])
            else:
                stats_str = self.pattern_stats.format(stats_str, k, 0, 0, 0)

        daemon.logger.info(
            "Component '{}': *** Processing statistics ***{}".format(
                self.cid,
                stats_str
            )
        )
        return (daemon.FLAG_CONTINUE, args)


class UuidGenerator:
    BASE_EVENT_NAME = "CTI-IntelMQFeed4"

    def __init__(self, idea_event: mentat.idea.internal.Idea, logger):
        self.logger = logger
        # map src_ips of idea_event to UUIDs of organizations in ResolvedAbuses
        src_ip_to_uuid = {}
        src_ips = idea_event.get_addresses(node="Source", get_v4=True, get_v6=False)
        org_uuids = idea_event.get_jpath_values("_Mentat.ResolvedAbuses")
        for src_ip, org_uuid in zip(src_ips, org_uuids):
            src_ip_to_uuid[str(src_ip)] = org_uuid if org_uuid else None
        self.src_ip_to_uuid = src_ip_to_uuid

    def get_org_uuid(self, src_ip: str) -> Optional[str]:
        """ Retrieve uuid of organization based on source IP. """
        return self.src_ip_to_uuid[src_ip]

    def get_misp_event_uuid(self, org_uuid: str) -> str:
        return str(uuid5(namespace=UUID(org_uuid), name=self.BASE_EVENT_NAME))

    def get_misp_obj_uuid(self, misp_event_uuid: str, src_ip: str, dst_ip, dst_port: int) -> str:
        name = "_-_".join((src_ip, dst_ip, str(dst_port)))
        return str(uuid5(namespace=UUID(misp_event_uuid), name=name))

    def get_misp_attr_uuid(self, misp_obj_uuid: str, attr_value: str) -> str:
        return str(uuid5(namespace=UUID(misp_obj_uuid), name=attr_value))


class IdeaToMispProcessor:
    def __init__(self, daemon_logger, misp_inst: ExpandedPyMISP, uuid_generator: UuidGenerator):
        self.logger = daemon_logger
        self.misp_inst = misp_inst
        self.uuid_generator = uuid_generator

    def _get_ips_and_ports(self, idea_event: mentat.idea.internal.Idea) -> Optional[Tuple[list, list, list]]:
        """
        Every message has to contain three attributes, if it wants to be processed: source IP, dest IP and dest port.
        One combination is enough, but at least one is necessary.
        :param idea_event: tested idea event
        :return: True or False based on presence of three attributes
        """
        if not idea_event.get_jpath_values("_Mentat.ResolvedAbuses"):
            self.logger.info(f"Idea message with uuid {idea_event.get_id()} cannot processed, because does not "
                             f"contain ResolvedAbuses!")
            return None
        src_ips = [str(ip) for ip in idea_event.get_addresses("Source", get_v4=True, get_v6=False)]
        dst_ips = [str(ip) for ip in idea_event.get_addresses("Target", get_v4=True, get_v6=False)]
        ports = idea_event.get_ports("Target")
        if not all((src_ips, dst_ips, ports)):
            self.logger.debug("Cannot process IDEA event - not enough attributes (at least on of SRC IP, DST IP, DST "
                             "port is missing)!")
            return None
        return src_ips, dst_ips, ports

    def _get_all_three_tuples_from_idea(self, src_ips, dst_ips, dst_ports) -> Set[Tuple[str, str, str]]:
        """ Get all possible combinations of src ips, dst ips and dst ports. """
        self.logger.debug(f"src ips: {src_ips}\ndst_ips: {dst_ips}\ndst_ports: {dst_ports}")
        new_objects_all_combinations = set()
        for src_ip in src_ips:
            for dst_ip in dst_ips:
                for dst_port in dst_ports:
                    new_objects_all_combinations.add((src_ip, dst_ip, dst_port))
        return new_objects_all_combinations

    def _add_sighting_to_existing_attr(self, obj: MISPObject) -> bool:
        """
        Adds positive sighting to source ip of passed object.
        :param obj: MISP object on which will be updated sighting
        :return: Boolean flag indicating, if the sighting update was successful or not
        """
        for attr in obj.Attribute:
            if attr.object_relation == "ip-src":
                sighting = attr.add_sighting({"id": attr.id, 'type': 0})
                resp = self.misp_inst.add_sighting(sighting, attr)
                if "Sighting" not in resp:
                    self.logger.error(f"Could not add sighting to object {obj.id}, because {resp}!")
                    return False
                else:
                    self.logger.debug(f"Sighting added to object {obj.uuid} in event {obj.event_id}!")
                return True
        return False

    def _create_new_misp_object(self, values: tuple, obj_uuid: str, misp_event: MISPEvent):
        """ Creates new MISP object with sighting on src ip. """
        attrs = {
            'ip-src': values[0],
            'ip-dst': values[1],
            'dst-port': values[2]
        }
        misp_obj = MISPObject(name="ip-port", strict=True)
        for attr_name, value in attrs.items():
            # TODO add concrete uuid to the attribute?
            misp_obj.add_attribute(object_relation=attr_name, value=value)
        misp_obj.uuid = obj_uuid
        res = self.misp_inst.add_object(misp_event, misp_obj, pythonify=True)
        self.logger.debug(f"Result of creating new misp object: {res}!")

    def _add_sightings_to_objects(self, three_tuples: list, misp_event: MISPEvent) -> int:
        """ Add sighting to all three tuples. """
        objs_to_update = {}
        # get MISP object uuid for all three tuples --> [obj_uuid] = three_tuple
        for three_tuple in three_tuples:
            obj_uuid = self.uuid_generator.get_misp_obj_uuid(misp_event.uuid, three_tuple[0], three_tuple[1],
                                                             three_tuple[2])
            objs_to_update[obj_uuid] = three_tuple

        # first go through events objects and if some match by uuid is found, update sightings and pop it from obj dict
        # --> means it is processed
        updated_count = 0
        for obj in misp_event.objects:
            if obj.uuid in objs_to_update.keys():
                objs_to_update.pop(obj.uuid)
                added_flag = self._add_sighting_to_existing_attr(obj)
                if added_flag:
                    updated_count += 1
        # for the rest of the three tuples create new MISP objects
        for obj_uuid, three_tuple in objs_to_update.items():
            self._create_new_misp_object(three_tuple, obj_uuid, misp_event)
        self.misp_inst.publish(misp_event)
        self.logger.debug(f"Event {misp_event.id} published after adding sightings to objects!")

        return updated_count

    def _create_new_event(self, org_uuid) -> MISPEvent:
        """ Creates new MISP event. """
        misp_event = MISPEvent()
        # TODO turn on correct organization assignment
        # misp_event.orgc = self.misp_inst.get_organisation(org_uuid, pythonify=True)
        # completed
        misp_event.analysis = 2
        # low
        misp_event.threat_level_id = 3
        # TODO use sharing group instead
        misp_event.distribution = 1
        # misp_event.distribution = 4
        # misp_event.sharing_group_id = 2
        misp_event.uuid = self.uuid_generator.get_misp_event_uuid(org_uuid)

        misp_event.add_tag("rsit:test")
        misp_event.add_tag("tlp:amber")

        misp_event.info = "CTI - IntelMQ feed"
        return self.misp_inst.add_event(misp_event, pythonify=True)

    def _create_new_event_with_object(self, three_tuple, org_uuid):
        """ Creates new MISP event with ip-port MISP object, which carries values from three_tuple. """
        misp_event = self._create_new_event(org_uuid)
        self.logger.info(f"Created event: {misp_event}")
        if isinstance(misp_event, dict) and misp_event.get('errors'):
            self.logger.warning(f"New event could not be created, probably because event with uuid "
                             f"{self.uuid_generator.get_misp_event_uuid(org_uuid)} have existed"
                             f" earlier and cannot be created again or for some other reason!")
            return
        obj_uuid = self.uuid_generator.get_misp_obj_uuid(misp_event.uuid, three_tuple[0], three_tuple[1], three_tuple[2])
        self._create_new_misp_object(three_tuple, obj_uuid, misp_event)
        self.misp_inst.publish(misp_event)

    def _get_events_to_update(self, three_tuples: list) -> dict:
        """
        Gets MISP events for all three tuples and assigns these tuples to misp event under one common key
        (org_uuid, misp_event_uuid): {'ev': misp_event, 'objs': [three_tuple1, three_tuple2, ...]}.
        """
        misp_events_to_update = {}
        for attr_tuple in three_tuples:
            org_uuid = self.uuid_generator.get_org_uuid(attr_tuple[0])
            if org_uuid is None:
                # UUID could not be found in GCAS API, skip this tuple
                continue

            misp_event_uuid = self.uuid_generator.get_misp_event_uuid(org_uuid)
            # get misp event object
            if (org_uuid, misp_event_uuid) not in misp_events_to_update.keys():
                misp_event = self.misp_inst.get_event(misp_event_uuid, pythonify=True)
                misp_events_to_update[(org_uuid, misp_event_uuid)] = {'ev': misp_event}
            # create list of three tuples, which belong to the event
            try:
                misp_events_to_update[(org_uuid, misp_event_uuid)]['objs'].append(attr_tuple)
            except KeyError:
                misp_events_to_update[(org_uuid, misp_event_uuid)]['objs'] = [attr_tuple]
        return misp_events_to_update

    def process_all_three_tuples(self, three_tuples: list):
        misp_events_to_update = self._get_events_to_update(three_tuples)
        if not misp_events_to_update:
            self.logger.info(f"Org UUID was not found for any src IP in GCAS API, terminate processing of this message.")
            return
        if len(three_tuples) == 1:
            # if only one three tuple, get its key
            org_uuid, misp_event_uuid = list(misp_events_to_update.keys())[0]
            if misp_events_to_update[(org_uuid, misp_event_uuid)]['ev'].get('errors'):
                # check if event exists (error will be in structure if event does not exist) --> create new event
                self._create_new_event_with_object(three_tuples[0], org_uuid)
                return

        # if there are more tuples, just add sightings to them
        for keys, ev_and_objs in misp_events_to_update.items():
            misp_ev_to_update = ev_and_objs['ev']
            if misp_ev_to_update.get('errors'):
                # event does not exist, skip this three tuple
                continue
            self._add_sightings_to_objects(ev_and_objs['objs'], misp_ev_to_update)

    def process_idea_event(self, idea_event: mentat.idea.internal.Idea):
        """ Find all three tuples of src ips, dst ips and dst ports, try to update sightings in MISP of those, which
         already exist in MISP or if the three tuple is only one, create the object if it does not exist already. """
        self.logger.debug(f"Starting processing idea event (uuid: {idea_event.get_id()})")
        try:
            src_ips, dst_ips, dst_ports = self._get_ips_and_ports(idea_event)
        except TypeError:
            return None
        all_three_tuples = self._get_all_three_tuples_from_idea(src_ips, dst_ips, dst_ports)
        self.process_all_three_tuples(list(all_three_tuples))
