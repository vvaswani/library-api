<?php

namespace App\DataFixtures;

use App\Entity\Book;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;

class BookFixtures extends Fixture
{
    public function load(ObjectManager $manager): void
    {
        $book = new Book();
        $book->setTitle("The Eagle Has Landed");
        $book->setAuthor("Jack Higgins");
        $manager->persist($book);

        $book = new Book();
        $book->setTitle("Carrie");
        $book->setAuthor("Stephen King");
        $manager->persist($book);

        $manager->flush();
    }
}
