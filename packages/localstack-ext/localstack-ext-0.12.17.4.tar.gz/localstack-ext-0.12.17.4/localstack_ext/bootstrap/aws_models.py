from localstack.utils.aws import aws_models
iOgcv=super
iOgcQ=None
iOgcu=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  iOgcv(LambdaLayer,self).__init__(arn)
  self.cwd=iOgcQ
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.iOgcu.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(RDSDatabase,self).__init__(iOgcu,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(RDSCluster,self).__init__(iOgcu,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(AppSyncAPI,self).__init__(iOgcu,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(AmplifyApp,self).__init__(iOgcu,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(ElastiCacheCluster,self).__init__(iOgcu,env=env)
class TransferServer(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(TransferServer,self).__init__(iOgcu,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(CloudFrontDistribution,self).__init__(iOgcu,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,iOgcu,env=iOgcQ):
  iOgcv(CodeCommitRepository,self).__init__(iOgcu,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
