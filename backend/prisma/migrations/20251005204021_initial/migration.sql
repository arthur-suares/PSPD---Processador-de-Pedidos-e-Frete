-- CreateTable
CREATE TABLE "Produto" (
    "id" TEXT NOT NULL DEFAULT gen_random_uuid(),
    "nome" TEXT NOT NULL,
    "descricao" TEXT,
    "preco" DOUBLE PRECISION NOT NULL,
    "estoque" INTEGER NOT NULL DEFAULT 0,
    "criadoEm" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "atualizadoEm" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Produto_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Estoque" (
    "id" TEXT NOT NULL DEFAULT gen_random_uuid(),
    "produtoId" TEXT NOT NULL,
    "quantidade" INTEGER NOT NULL,
    "localizacao" TEXT,

    CONSTRAINT "Estoque_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Estoque" ADD CONSTRAINT "Estoque_produtoId_fkey" FOREIGN KEY ("produtoId") REFERENCES "Produto"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
