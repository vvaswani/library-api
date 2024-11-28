<?php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;
use App\Entity\Book;
use App\Repository\BookRepository;

class BookController extends AbstractController
{
    #[Route('/api/books', methods: ['GET'])]
    public function getBooks(BookRepository $bookRepository): Response
    {
        $books = $bookRepository->findAll();
        return $this->json($books);
    }

    #[Route('/api/books', methods: ['POST'])]
    public function addBook(Request $request, BookRepository $bookRepository): Response
    {
        $data = json_decode($request->getContent(), true);

        if (empty($data['title']) || empty($data['author'])) {
            return $this->json(['error' => 'Invalid request parameters'], 400);
        }

        $book = new Book();
        $book->setTitle($data['title']);
        $book->setAuthor($data['author']);

        $bookRepository->add($book);

        return $this->json($book, 201);
    }

    #[Route('/api/books/{id}', methods: ['DELETE'])]
    public function deleteBook(int $id, BookRepository $bookRepository): Response
    {
        $book = $bookRepository->findOneById($id);
        if (!$book) {
            return $this->json(['error' => 'Book not found'], 404);
        } else {
            $bookRepository->remove($book);
            return $this->json(null, 204);
        }
    }

    #[Route('/api/books/{id}', methods: ['GET'])]
    public function getBook(int $id, BookRepository $bookRepository): Response
    {
        $book = $bookRepository->findOneById($id);
        if (!$book) {
            return $this->json(['error' => 'Book not found'], 404);
        } else {
            return $this->json($book);
        }
    }

    #[Route('/api/books/{id}', methods: ['PUT'])]
    public function updateBook(int $id, Request $request, BookRepository $bookRepository): Response
    {
        $data = json_decode($request->getContent(), true);
        $book = $bookRepository->findOneById($id);
        if (!$book) {
            return $this->json(['error' => 'Book not found'], 404);
        } else {
            if (!empty($data['title'])) {
                $book->setTitle($data['title']);
            }
            if (!empty($data['author'])) {
                $book->setAuthor($data['author']);
            }
            $bookRepository->add($book);
            return $this->json($book);
        }
    }
}
