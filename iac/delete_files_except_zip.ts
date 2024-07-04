import { promises as fsPromises } from 'fs';
import { join } from 'path';

async function deleteFilesExceptZip(directory: string, zipFileName: string): Promise<void> {
  try {
    const filesAndFolders = await fsPromises.readdir(directory, { withFileTypes: true });

    for (const dirent of filesAndFolders) {
      const fullPath = join(directory, dirent.name);
      if (dirent.name !== zipFileName) {
        if (dirent.isDirectory()) {
          await fsPromises.rm(fullPath, { recursive: true, force: true });
        } else {
          await fsPromises.unlink(fullPath);
        }
      }
    }

    console.log('Todos os arquivos e pastas deletados, exceto o arquivo ZIP.');
  } catch (error) {
    console.error('Erro ao deletar arquivos e pastas:', error);
    throw error;
  }

}

// Exemplo de uso da função
export async function cleanUpDirectory(directoryPath: string, zipFileName: string) {
  try {
    await deleteFilesExceptZip(directoryPath, zipFileName);
    console.log('Diretório limpo com sucesso.');
  } catch (error) {
    console.error('Falha ao limpar o diretório.', error);
  }
}