import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';
import { cleanUpDirectory } from './delete_files_except_zip';
import { createZip } from './create_zip';

const IAC_DIRECTORY_NAME = 'iac';
const SOURCE_DIRECTORY_NAME = 'src';
const SHARED_DIR_NAME = 'shared';
const SHARED_PYTHON_DIR_NAME = 'python';
const SQLALCHEMY_DIR_NAME = 'sqlalchemy';
const SITE_PACKAGES_DIR_NAMES = ['python', 'lib', 'python3.11', 'site-packages'];
const ZIP_FILE_NAME = 'requirements.zip';

export function adjustLayerDirectory(): void {
  // Obtém o diretório raiz do diretório fonte
  const rootDirectory = path.join(__dirname, '..');
  const iacDirectory = path.join(rootDirectory, IAC_DIRECTORY_NAME);

  console.log(`Root directory: ${rootDirectory}`);
  console.log(`Root directory files: ${fs.readdirSync(rootDirectory)}`);
  console.log(`IaC directory: ${iacDirectory}`);
  console.log(`IaC directory files: ${fs.readdirSync(iacDirectory)}`);

  // Define os diretórios de origem e destino para shared
  const sourceDirectory = path.join(rootDirectory, SOURCE_DIRECTORY_NAME, SHARED_DIR_NAME);
  const destinationDirectory = path.join(iacDirectory, SHARED_DIR_NAME, SHARED_PYTHON_DIR_NAME, SOURCE_DIRECTORY_NAME, SHARED_DIR_NAME);

  // Apaga o diretório de destino se ele existir
  if (fs.existsSync(destinationDirectory)) {
    fs.rmSync(destinationDirectory, { recursive: true, force: true });
  }

  // Cria o diretório de destino
  fs.mkdirSync(destinationDirectory, { recursive: true });

  // Copia o diretório fonte para o diretório de destino
  console.log(`Copying files from ${sourceDirectory} to ${destinationDirectory}`);
  copyFolderSync(sourceDirectory, destinationDirectory);

  // Cria e ajusta o diretório para sqlalchemy
  const sqlalchemySitePackagesDir = path.join(iacDirectory, SQLALCHEMY_DIR_NAME, ...SITE_PACKAGES_DIR_NAMES);

  if (fs.existsSync(sqlalchemySitePackagesDir)) {
    fs.rmSync(sqlalchemySitePackagesDir, { recursive: true, force: true });
  }

  fs.mkdirSync(sqlalchemySitePackagesDir, { recursive: true });

  // Instala as bibliotecas do requirements.txt
  installRequirements(rootDirectory, sqlalchemySitePackagesDir)
    .then(() => {
      // Cria o arquivo ZIP dentro do diretório sqlalchemy
      return createZip(sqlalchemySitePackagesDir, ZIP_FILE_NAME);
    })
    .then(() => {
      // Limpa o diretório, exceto pelo arquivo ZIP
      return cleanUpDirectory(sqlalchemySitePackagesDir, ZIP_FILE_NAME);
    })
    .catch(error => {
      console.error('Falha ao ajustar o diretório da camada:', error);
    });
}

function copyFolderSync(src: string, dest: string): void {
  fs.mkdirSync(dest, { recursive: true });
  const files = fs.readdirSync(src);

  for (const file of files) {
    const current = fs.lstatSync(path.join(src, file));

    if (current.isDirectory()) {
      copyFolderSync(path.join(src, file), path.join(dest, file));
    } else if (current.isSymbolicLink()) {
      const symlink = fs.readlinkSync(path.join(src, file));
      fs.symlinkSync(symlink, path.join(dest, file));
    } else {
      fs.copyFileSync(path.join(src, file), path.join(dest, file));
    }
  }
}

async function installRequirements(rootDir: string, sitePackagesDir: string): Promise<void> {
  const requirementsFile = path.join(rootDir, 'requirements.txt');
  if (!fs.existsSync(requirementsFile)) {
    throw new Error(`requirements.txt not found in ${rootDir}`);
  }

  try {
    const command = `pip install -r ${requirementsFile} --target ${sitePackagesDir}`;
    console.log(`Running command: ${command}`);
    execSync(command, { stdio: 'inherit' });
    console.log(`Successfully installed requirements from ${requirementsFile} to ${sitePackagesDir}`);
  } catch (error) {
    console.error(`Failed to install requirements: ${error}`);
    throw error;
  }
}

if (require.main === module) {
  adjustLayerDirectory();
}
