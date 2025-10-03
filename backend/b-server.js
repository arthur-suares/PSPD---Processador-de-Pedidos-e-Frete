import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const packageDef = protoLoader.loadSync("proto/service.proto");
const grpcObj = grpc.loadPackageDefinition(packageDef).services;

function calculate(call, callback) {
  const input = call.request.input;
  const result = `Resultado B: ${input.length}`;
  callback(null, { output: result });
}

const server = new grpc.Server();
server.addService(grpcObj.ServiceB.service, { Calculate: calculate });

server.bindAsync("0.0.0.0:50052", grpc.ServerCredentials.createInsecure(), () => {
  console.log("Server B rodando em 50052");
  server.start();
});
