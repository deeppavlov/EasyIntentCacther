import paramiko
import os
from django.conf import settings


class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        '''
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise


def upload_to_ssh_recursive(model_path):
    transport = paramiko.Transport((settings.SSH_HOST, settings.SSH_PORT))
    transport.connect(username=settings.SSH_USERNAME, password=settings.SSH_PASSWORD)
    sftp = MySFTPClient.from_transport(transport)

    model_code = model_path.split("/")[-1]
    target_path = settings.SSH_EXPORT_TARGET_BASE_PATH+model_code
    print('target_path')
    print(target_path)
    sftp.mkdir(target_path, ignore_existing=True)
    print(f"Sending model {model_path} to ssh {target_path}:")
    sftp.put_dir(model_path, target_path)
    sftp.close()