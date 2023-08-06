from localstack.utils.aws import aws_models
LeTlx=super
LeTlS=None
LeTlz=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  LeTlx(LambdaLayer,self).__init__(arn)
  self.cwd=LeTlS
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.LeTlz.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(RDSDatabase,self).__init__(LeTlz,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(RDSCluster,self).__init__(LeTlz,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(AppSyncAPI,self).__init__(LeTlz,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(AmplifyApp,self).__init__(LeTlz,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(ElastiCacheCluster,self).__init__(LeTlz,env=env)
class TransferServer(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(TransferServer,self).__init__(LeTlz,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(CloudFrontDistribution,self).__init__(LeTlz,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,LeTlz,env=LeTlS):
  LeTlx(CodeCommitRepository,self).__init__(LeTlz,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
