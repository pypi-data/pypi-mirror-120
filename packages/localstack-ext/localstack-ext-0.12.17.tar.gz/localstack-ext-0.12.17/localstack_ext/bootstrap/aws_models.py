from localstack.utils.aws import aws_models
dPstB=super
dPstM=None
dPstO=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dPstB(LambdaLayer,self).__init__(arn)
  self.cwd=dPstM
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dPstO.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(RDSDatabase,self).__init__(dPstO,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(RDSCluster,self).__init__(dPstO,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(AppSyncAPI,self).__init__(dPstO,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(AmplifyApp,self).__init__(dPstO,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(ElastiCacheCluster,self).__init__(dPstO,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(TransferServer,self).__init__(dPstO,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(CloudFrontDistribution,self).__init__(dPstO,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dPstO,env=dPstM):
  dPstB(CodeCommitRepository,self).__init__(dPstO,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
