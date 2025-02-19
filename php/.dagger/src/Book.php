<?php

declare(strict_types=1);

namespace DaggerModule;

use Dagger\Attribute\DaggerFunction;
use Dagger\Attribute\DaggerObject;
use Dagger\Attribute\Doc;
use Dagger\Attribute\DefaultPath;
use Dagger\Container;
use Dagger\Directory;

use function Dagger\dag;

#[DaggerObject]
#[Doc('A generated module for Book functions')]
class Book
{

    #[DaggerFunction]
    public function __construct(
        #[DefaultPath('.')]
        public Directory $source,
        public string $version = '8.3'
    ) {
    }

    #[DaggerFunction]
    #[Doc('Returns a PHP env with dependencies and source code')]
    public function env(): Container
    {
        return dag()
            ->container()
            // use php base image
            ->from('php:' . $this->version . '-cli')
            // mount caches
            ->withMountedCache('/root/.composer', dag()->cacheVolume('composer-php'))
            ->withMountedCache('/var/cache/apt', dag()->cacheVolume('apt'))
            ->withExec(['apt-get', 'update'])
            // install system deps
            ->withExec(['apt-get', 'install', '--yes', 'git-core', 'zip', 'curl'])
            // install php deps
            ->withExec(['apt-get', 'install', '--yes', 'libpq-dev'])
            ->withExec(['docker-php-ext-install', 'pdo_pgsql'])
            // install composer
            ->withExec(['sh', '-c', 'curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer'])
            // mount source code and set workdir
            ->withDirectory('/app', $this->source->withoutDirectory('.dagger'))
            ->withWorkdir('/app')
            // install app deps
            ->withExec(['composer', 'install']);
    }

    #[DaggerFunction]
    #[Doc('Returns the result of unit tests')]
    public function test(): string {

        $postgresdb = dag()
            ->container()
            // use postgres image
            ->from('postgres:alpine')
            // create default db for tests
            // as per symfony conventions, db name is with _test suffix
            ->withEnvVariable('POSTGRES_DB', 'app_test')
            ->withEnvVariable('POSTGRES_PASSWORD', 'secret')
            ->withExposedPort(5432)
            // start service
            ->asService([], true);

        return $this
            ->env()
            // bind to postgres service
            ->withServiceBinding('db', $postgresdb)
            // set env=test
            ->withEnvVariable('APP_ENV', 'test')
            //->withEnvVariable('DATABASE_URL', 'postgres://postgres:secret@db:5432/app_test')
            // populate db with test data
            ->withExec(['./bin/console', 'doctrine:schema:create'])
            // run unit tests
            ->withExec(['composer', 'require', '--dev', 'phpunit/phpunit'])
            ->withExec(['./vendor/bin/phpunit'])
            ->stdout();
    }
}
