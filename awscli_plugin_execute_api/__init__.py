import types
import logging
from botocore.auth import SigV4Auth

logger = logging.getLogger("awscli.clidriver")

def get_auth_instance(self, signing_name, region_name, signature_version=None, **kwargs):
    # create new signer for API Gateway
    # addresses `Credential should be scoped to correct service: 'execute-api'` error
    return SigV4Auth(self._credentials, "execute-api", region_name)

def building_argument_table(argument_table, operation_model, event_name, session, **kwargs):
    cfg = session.get_scoped_config()

    evt = event_name.split(".")   # building-argument-table.dynamodb.update-table
    svc = evt[1]                  # dynamodb
    op  = evt[2]                  # update-table
    opName = operation_model.name # UpdateTable

    try:
        url = cfg[svc][op]
        logger.debug("Plugin awscli_plugin_execute_api: Config [%s] %s.%s => URL %s", session.profile, svc, op, url)
    except KeyError:
        logger.debug("Plugin awscli_plugin_execute_api: Config [%s] %s.%s not found", session.profile, svc, op)
        return

    # build and register a before-sign hook that modifies the request URL and monkeypatches the request signer
    def before_sign(request, operation_name, **kwargs):
        request.url = url

        # Rename transport header. Addresses:
        # The service name : "BackplaneExecutionService" identified from the payload does not agree with the service name : "DynamoDB_20120810" specified in the transport header
        if "X-Amz-Target" in request.headers:
            request.headers["X-Target"] = request.headers["X-Amz-Target"]
            del request.headers["X-Amz-Target"]
            logger.debug("Plugin awscli_plugin_execute_api: renamed X-Amz-Target %s", request.headers["X-Target"])

        # patch signer and auth
        signer = kwargs['request_signer']
        signer.get_auth_instance = types.MethodType(get_auth_instance, signer)

    session.register("before-sign.%s.%s" % (svc, opName), before_sign)

def awscli_initialize(cli):
    cli.register("building-argument-table", building_argument_table)
