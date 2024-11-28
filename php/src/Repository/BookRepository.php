<?php

namespace App\Repository;

use App\Entity\Book;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<Book>
 */
class BookRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Book::class);
    }

    public function add(Book $book): void
    {
        $entityManager = $this->getEntityManager();
        $entityManager->persist($book);
        $entityManager->flush();
    }

    public function remove(Book $book): void
    {
        $entityManager = $this->getEntityManager();
        $entityManager->remove($book);
        $entityManager->flush();
    }

    public function findOneById(int $id): ?Book
    {
        return $this->getEntityManager()
            ->getRepository(Book::class)
            ->find($id);
    }

    public function findAll(): array
    {
        return $this->getEntityManager()
          ->getRepository(Book::class)
          ->findBy([]);
    }
}
