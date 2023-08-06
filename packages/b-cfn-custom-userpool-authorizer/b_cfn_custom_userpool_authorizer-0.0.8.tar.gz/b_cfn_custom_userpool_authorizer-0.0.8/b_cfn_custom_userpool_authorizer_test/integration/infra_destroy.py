import os

from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_testing_framework.tools.cdk_testing.cdk_tool_config import CdkToolConfig

from b_cfn_custom_userpool_authorizer_test.integration.manager import MANAGER

DO_NOT_DESTROY_INFRASTRUCTURE = int(os.environ.get('DO_NOT_DESTROY_INFRASTRUCTURE', 0))


def inf_destroy():
    if DO_NOT_DESTROY_INFRASTRUCTURE == 1:
        return

    def wrapper(cdk_config: CdkToolConfig):
        DeploymentExecutor(
            type=DeploymentType.DESTROY,
            path=cdk_config.cdk_app_path,
            env=cdk_config.deployment_process_environment,
        ).run()

    MANAGER.destroy_infrastructure(wrapper)


if __name__ == '__main__':
    inf_destroy()
