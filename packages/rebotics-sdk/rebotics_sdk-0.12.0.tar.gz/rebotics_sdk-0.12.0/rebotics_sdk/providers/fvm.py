from rebotics_sdk.providers import ReboticsBaseProvider, remote_service


class FeatureVectorManagerProvider(ReboticsBaseProvider):
    @remote_service('/api/token-auth/')
    def login(self, username, password):
        response = self.session.post()
