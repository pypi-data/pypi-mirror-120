from localstack.utils.aws import aws_models
VHKwX=super
VHKwC=None
VHKwA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  VHKwX(LambdaLayer,self).__init__(arn)
  self.cwd=VHKwC
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.VHKwA.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(RDSDatabase,self).__init__(VHKwA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(RDSCluster,self).__init__(VHKwA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(AppSyncAPI,self).__init__(VHKwA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(AmplifyApp,self).__init__(VHKwA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(ElastiCacheCluster,self).__init__(VHKwA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(TransferServer,self).__init__(VHKwA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(CloudFrontDistribution,self).__init__(VHKwA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,VHKwA,env=VHKwC):
  VHKwX(CodeCommitRepository,self).__init__(VHKwA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
