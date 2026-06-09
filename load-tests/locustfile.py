import time
from locust import HttpUser, task, between
import grpc
import streaming_pb2
import streaming_pb2_grpc

class StreamingTester(HttpUser):
    wait_time = between(0.5, 2)

    def on_start(self):
        # Conecta aos servidores gRPC
        self.node_grpc_channel = grpc.insecure_channel("node-grpc:50051")
        self.node_grpc_stub = streaming_pb2_grpc.StreamingServiceStub(self.node_grpc_channel)

        self.py_grpc_channel = grpc.insecure_channel("python-grpc:50052")
        self.py_grpc_stub = streaming_pb2_grpc.StreamingServiceStub(self.py_grpc_channel)

    # Função Auxiliar para forçar o gRPC a aparecer na tabela
    def track_grpc(self, name, stub_method):
        start_time = time.time()
        try:
            stub_method(streaming_pb2.Empty())
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(request_type="gRPC", name=name, response_time=total_time, response_length=0, exception=None)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            self.environment.events.request.fire(request_type="gRPC", name=name, response_time=total_time, response_length=0, exception=e)

    # ==========================
    # 1. REST
    # ==========================
    @task(1)
    def test_rest_node(self):
        self.client.get("http://node-rest:3000/usuarios", name="1. REST (Node.js)")

    @task(1)
    def test_rest_py(self):
        self.client.get("http://python-rest:8000/usuarios", name="2. REST (Python)")

    # ==========================
    # 2. GraphQL
    # ==========================
    @task(1)
    def test_graphql_node(self):
        self.client.post("http://node-graphql:3001/graphql", json={"query": "{ usuarios { id nome } }"}, name="3. GraphQL (Node.js)")

    @task(1)
    def test_graphql_py(self):
        self.client.post("http://python-graphql:8001/graphql", json={"query": "{ usuarios { id nome } }"}, name="4. GraphQL (Python)")

    # ==========================
    # 3. SOAP
    # ==========================
    @task(1)
    def test_soap_node(self):
        xml = """<?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://streaming.soap">
           <soapenv:Body><tns:ListarUsuarios/></soapenv:Body>
        </soapenv:Envelope>"""
        
        headers = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": '""'}
        
        with self.client.post("http://node-soap:3002/wsdl", data=xml, headers=headers, name="5. SOAP (Node.js)", catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Falha no Node. XML Retornado: {res.text}")

    @task(1)
    def test_soap_py(self):
        # O segredo estava no xmlns:tns="streaming.soap.example"
        xml = """<?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="streaming.soap.example">
           <soapenv:Body><tns:ListarUsuarios/></soapenv:Body>
        </soapenv:Envelope>"""
        
        headers = {
            "Content-Type": "text/xml; charset=utf-8", 
            "SOAPAction": '"ListarUsuarios"' 
        }
        
        with self.client.post("http://python-soap:8002/", data=xml, headers=headers, name="6. SOAP (Python)", catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"Falha no Python. XML: {res.text}")

    # ==========================
    # 4. gRPC
    # ==========================
    @task(1)
    def test_grpc_node(self):
        self.track_grpc("7. gRPC (Node.js)", self.node_grpc_stub.ListarUsuarios)

    @task(1)
    def test_grpc_py(self):
        self.track_grpc("8. gRPC (Python)", self.py_grpc_stub.ListarUsuarios)