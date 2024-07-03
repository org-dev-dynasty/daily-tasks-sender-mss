import { exec } from 'child_process';
import { promisify } from 'util';

// Converte exec para uma versão que retorna Promises usando promisify
const execAsync = promisify(exec);

// Função assíncrona para executar um comando shell
async function runShellCommand(command: string): Promise<void> {
  try {
    const { stdout, stderr } = await execAsync(command);
    console.log(stdout);
    if (stderr) {
      console.error(`Stderr: ${stderr}`);
    }
  } catch (error) {
    console.error(`Erro ao executar o comando: ${error}`);
    throw error; // Re-lança o erro para ser tratado pelo chamador da função
  }
}

// Exemplo de uso da função assíncrona para criar um arquivo ZIP
export async function createZip(pathToSitePackages: string, zipFileName: string) {
  const zipCommand = `cd ${pathToSitePackages} && zip -r ${zipFileName} .`;

  try {
    await runShellCommand(zipCommand);
    console.log('Arquivo ZIP criado com sucesso.');
  } catch (error) {
    console.error('Falha ao criar o arquivo ZIP.', error);
  }
}
