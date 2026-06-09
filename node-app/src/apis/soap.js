const express = require('express');
const soap = require('soap');
const services = require('../services');

const myService = {
  StreamingService: {
    StreamingPort: {
      ListarUsuarios: async function(args, callback) {
        const usuarios = await services.listarUsuarios();
        callback({ usuarios: usuarios });
      },
      ListarMusicas: async function(args, callback) {
        const musicas = await services.listarMusicas();
        callback({ musicas: musicas });
      }
    }
  }
};

const xml = `
<definitions name="StreamingService"
  targetNamespace="http://www.examples.com/wsdl/StreamingService.wsdl"
  xmlns="http://schemas.xmlsoap.org/wsdl/"
  xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:tns="http://www.examples.com/wsdl/StreamingService.wsdl"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <message name="EmptyRequest"></message>
  <message name="UsuarioResponse"><part name="usuarios" type="xsd:string"/></message>
  <message name="MusicaResponse"><part name="musicas" type="xsd:string"/></message>
  
  <portType name="StreamingPortType">
    <operation name="ListarUsuarios">
      <input message="tns:EmptyRequest"/>
      <output message="tns:UsuarioResponse"/>
    </operation>
    <operation name="ListarMusicas">
      <input message="tns:EmptyRequest"/>
      <output message="tns:MusicaResponse"/>
    </operation>
  </portType>

  <binding name="StreamingBinding" type="tns:StreamingPortType">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="ListarUsuarios">
      <soap:operation soapAction="ListarUsuarios"/>
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
    <operation name="ListarMusicas">
      <soap:operation soapAction="ListarMusicas"/>
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
  </binding>

  <service name="StreamingService">
    <port name="StreamingPort" binding="tns:StreamingBinding">
      <soap:address location="http://localhost:3002/wsdl"/>
    </port>
  </service>
</definitions>
`;

const app = express();
app.listen(3002, function(){
  soap.listen(app, '/wsdl', myService, xml, function(){
    console.log('SOAP Node.js rodando na porta 3002');
  });
});