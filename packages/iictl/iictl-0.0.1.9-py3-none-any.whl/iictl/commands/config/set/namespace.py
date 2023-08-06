import click
from iictl.commands.config.set.main import set
from iictl.kubectl.kubectl import get_kubectl_config_namespace_replace, get_executable, get_kubectl_config_current_context
from iictl.utils.kube import verify_object_name

@set.command(help='set current namespace')
@click.argument('namespace')
def namespace(namespace):
    verify_object_name(namespace)
    
    executable = get_executable()
    # TODO: listing ii with name and error if ii is not exist or deployment is not ready
    if executable:
        # TODO: logging change to use logging module
        import subprocess
        
        current_context = subprocess.check_output(get_kubectl_config_current_context(executable)).decode('utf-8').strip()
        
        kubectl_command = get_kubectl_config_namespace_replace(
            namespace=namespace,
            executable=executable,
            current_context=current_context,
        )
        
        subprocess.call(kubectl_command)
    else:
        raise NotImplementedError