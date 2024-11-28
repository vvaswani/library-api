<?php

namespace App\Tests\Controller;

use App\Entity\Book;
use App\Repository\BookRepository;
use Symfony\Bundle\FrameworkBundle\KernelBrowser;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;
use Symfony\Component\HttpFoundation\Response;

class BookControllerTest extends WebTestCase
{
    private KernelBrowser $client;
    private BookRepository $bookRepository;

    protected function setUp(): void
    {
        $this->client = self::createClient();
        $container = static::getContainer();
        $this->bookRepository = $container->get(BookRepository::class);
    }

    public function testGetBooks(): void
    {
        $this->client->request('GET', '/api/books');
        $this->assertResponseIsSuccessful();
        $this->assertJsonResponse();
    }

    public function testGetBookValid(): void
    {
        $book = new Book();
        $book->setTitle('The Martian')->setAuthor('Andy Weir');
        $this->bookRepository->add($book);

        $this->client->request('GET', '/api/books/' . $book->getId());
        $this->assertResponseIsSuccessful();
        $this->assertJsonResponse();

        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('The Martian', $responseData['title']);
        $this->assertEquals('Andy Weir', $responseData['author']);
    }

    public function testGetBookNotFound(): void
    {
        $this->client->request('GET', '/api/books/99999');
        $this->assertResponseStatusCodeSame(Response::HTTP_NOT_FOUND);

        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('Book not found', $responseData['error']);
    }

    public function testAddBookValid(): void
    {
        $this->client->request('POST', '/api/books', [], [], ['CONTENT_TYPE' => 'application/json'], json_encode([
            'title' => 'The Martian',
            'author' => 'Andy Weir',
        ]));

        $this->assertResponseStatusCodeSame(Response::HTTP_CREATED);
        $this->assertJsonResponse();

        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('The Martian', $responseData['title']);
        $this->assertEquals('Andy Weir', $responseData['author']);
    }

    public function testAddBookInvalid(): void
    {
        $this->client->request('POST', '/api/books', [], [], ['CONTENT_TYPE' => 'application/json'], json_encode([]));
        $this->assertResponseStatusCodeSame(Response::HTTP_BAD_REQUEST);

        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('Invalid request parameters', $responseData['error']);
    }

    public function testDeleteBookValid(): void
    {
        $book = new Book();
        $book->setTitle('The Martian')->setAuthor('Andy Weir');
        $this->bookRepository->add($book);

        $this->client->request('DELETE', '/api/books/' . $book->getId());
        $this->assertResponseStatusCodeSame(Response::HTTP_NO_CONTENT);
    }

    public function testDeleteBookNotFound(): void
    {
        $this->client->request('DELETE', '/api/books/99999');
        $this->assertResponseStatusCodeSame(Response::HTTP_NOT_FOUND);

        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('Book not found', $responseData['error']);
    }

    public function testUpdateBookValid(): void
    {
        $book = new Book();
        $book->setTitle('The Martian')->setAuthor('Andy Weir');
        $this->bookRepository->add($book);

        $this->client->request('PUT', '/api/books/' . $book->getId(), [], [], ['CONTENT_TYPE' => 'application/json'], json_encode([
            'title' => 'The Martian Updated',
            'author' => 'Andy Weir',
        ]));

        $this->assertResponseIsSuccessful();
        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('The Martian Updated', $responseData['title']);
    }

    public function testUpdateBookNotFound(): void
    {
        $this->client->request('PUT', '/api/books/99999', [], [], ['CONTENT_TYPE' => 'application/json'], json_encode([
            'title' => 'Non-Existent Book',
            'author' => 'Unknown',
        ]));

        $this->assertResponseStatusCodeSame(Response::HTTP_NOT_FOUND);
        $responseData = json_decode($this->client->getResponse()->getContent(), true);
        $this->assertEquals('Book not found', $responseData['error']);
    }

    private function assertJsonResponse(): void
    {
        $this->assertEquals('application/json', $this->client->getResponse()->headers->get('Content-Type'));
    }
}
