pythonCopier le codefrom concurrent import futuresimport grpcimport egapro_pb2import egapro_pb2_grpc
# Fonction exemple pour récupérer les données EgaPro (à remplacer par la logique réelle)def fetch_egapro_data(siren):
    return f"Data for SIREN {siren}"# Classe de service implémentant le service EgaproService défini dans le fichier .protoclass EgaproServicer(egapro_pb2_grpc.EgaproServiceServicer):
    def GetEgaproData(self, request, context):
        data = fetch_egapro_data(request.siren)        return egapro_pb2.EgaproResponse(data=data)
# Fonction pour démarrer le serveur gRPCdef serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    egapro_pb2_grpc.add_EgaproServiceServicer_to_server(EgaproServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()