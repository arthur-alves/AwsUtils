# coding: utf-8
"""This module make your life simple when you need to use AWS.

This main use is recovery data from AWS EC2 instances, to start and stop
instances and much more. Not fully implemented yet.
"""
import os
import boto.ec2
import textwrap


class AwsUtils(object):
    u"""This tool provide some functions to use in AWS remotely."""

    def __init__(self, access_key, secret_key, region='sa-east-1'):
        """Arg init."""
        self.region = region
        self._instances_info = False
        self.conn = boto.ec2.connect_to_region(
            self.region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

        self._check_status()

    def _check_status(self):
        u"""Check connection status."""
        try:
            self.conn.get_all_instance_status()
            return True
        except Exception as err:
            raise ValueError("Connection error: {}".format(err.message))

    def start_service(self, workers_ids):
        """Start AWS EC2 instances."""
        self.conn.start_instances(instance_ids=workers_ids)

    def stop_service(self, workers_ids):
        u"""Start AWS EC2 instances."""
        self.conn.stop_instances(instance_ids=workers_ids)

    def get_all_instances_info(self, filter_name=False):
        u"""List all info of instances.

        Args:
            - filter @str: filter by instance's name.
        """
        def _filter(info):
            all_info = [info[i] for i in info if
                        i.startswith(filter_name)]

            return all_info

        # Cache recovery info
        if self._instances_info:
            if filter_name:
                return _filter(self._instances_info)
            return self._instances_info

        inst_info = []
        all_info = {}
        repeat_count = 0

        [inst_info.extend(i.instances) for i in self.conn.get_all_instances()]

        for instance in inst_info:
            inst_name = instance.tags.get("Name")

            # Avoid name overwrite in dict.
            if inst_name in all_info:
                repeat_count += 1
                inst_name = "{}-{}".format(inst_name, repeat_count)

            all_info[inst_name] = {}
            all_info[inst_name].update(instance.__dict__)

        self._instances_info = all_info

        if filter_name:
            return _filter(self._instances_info)

        return all_info

    def get_all_instances_ids(self):
        u"""Get all instance's ids in AWS EC2.

        Used in start e stop_service

        E.G.: To stop all insntances, use that:
            all_ids = self.get_all_instance_ids()
            self.start_service( all_ids.values() )
        """
        info = self.get_all_instances_info()
        instance_ids = {}
        for key, dic in info.iteritems():
            instance_ids[key] = dic.get("id")

        return instance_ids

    def generate_ssh_conf(self, save_path='/tmp/', ssh_path="~/.ssh/"):
        u"""Generate ssh conf in .

        Args:
            - save_path @string: path to save
            - ssh_path @string: path where find pem files

        """
        aws_info = self.get_all_instances_info()

        ssh_path = os.path.join(os.path.expanduser(ssh_path), "{}")
        file_name = os.path.join(save_path, 'config')
        conf_file = open(file_name, "w")
        header = "# File auto automatically generated with AwsUtils"
        conf_file.writelines(header)
        conf_info = """

            host {}
            hostname {}
            user ubuntu
            IdentityFile {}
        """
        conf_info = textwrap.dedent(conf_info)
        for count, name in enumerate(aws_info):
            # host alias without space
            host_name = "-".join(name.split())
            conf_file.writelines(conf_info.format(
                host_name,
                aws_info[name].get("ip_address"),
                os.path.join(
                    os.path.expanduser(
                        ssh_path.format(aws_info[name].get("key_name"))
                    )
                )
            ))

        conf_file.close()
