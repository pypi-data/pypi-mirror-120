from localstack.utils.aws import aws_models
utqIy=super
utqIw=None
utqIM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  utqIy(LambdaLayer,self).__init__(arn)
  self.cwd=utqIw
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.utqIM.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(RDSDatabase,self).__init__(utqIM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(RDSCluster,self).__init__(utqIM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(AppSyncAPI,self).__init__(utqIM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(AmplifyApp,self).__init__(utqIM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(ElastiCacheCluster,self).__init__(utqIM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(TransferServer,self).__init__(utqIM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(CloudFrontDistribution,self).__init__(utqIM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,utqIM,env=utqIw):
  utqIy(CodeCommitRepository,self).__init__(utqIM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
