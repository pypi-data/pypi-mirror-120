from localstack.utils.aws import aws_models
PSWnx=super
PSWne=None
PSWnm=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  PSWnx(LambdaLayer,self).__init__(arn)
  self.cwd=PSWne
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.PSWnm.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(RDSDatabase,self).__init__(PSWnm,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(RDSCluster,self).__init__(PSWnm,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(AppSyncAPI,self).__init__(PSWnm,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(AmplifyApp,self).__init__(PSWnm,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(ElastiCacheCluster,self).__init__(PSWnm,env=env)
class TransferServer(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(TransferServer,self).__init__(PSWnm,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(CloudFrontDistribution,self).__init__(PSWnm,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,PSWnm,env=PSWne):
  PSWnx(CodeCommitRepository,self).__init__(PSWnm,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
