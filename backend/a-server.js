import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const packageDef = protoLoader.loadSync("proto/service.proto");
const grpcObj = grpc.loadPackageDefinition(packageDef).services;

function doSomething(call, callback) {
  const input = call.request.input;
  callback(null, { output: `A processou: ${input}` });
}

const server = new grpc.Server();
server.addService(grpcObj.ServiceA.service, { DoSomething: doSomething });

server.bindAsync("0.0.0.0:50051", grpc.ServerCredentials.createInsecure(), () => {
  console.log("Server A rodando em 50051");
  server.start();
});
