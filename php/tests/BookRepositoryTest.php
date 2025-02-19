<?php
use App\Entity\Book;
use App\Repository\BookRepository;
use Symfony\Bundle\FrameworkBundle\Test\KernelTestCase;

class BookRepositoryTest extends KernelTestCase
{
  private BookRepository $bookRepository;

  protected function setUp(): void
  {
      self::bootKernel();
      $container = static::getContainer();
      $this->bookRepository = $container->get(BookRepository::class);
  }

    public function testFindAll(): void
    {
        $book = $this->createBook('The Eagle Has Landed', 'Jack Higgins');
        $this->bookRepository->add($book);

        $book = $this->createBook('Carrie', 'Stephen King');
        $this->bookRepository->add($book);

        $books = $this->bookRepository->findAll();
        $this->assertIsArray($books);
        $this->assertCount(2, $books);
        $this->assertInstanceOf(Book::class, $books[0]);
    }

    public function testFindOneByTitle(): void
    {
        $book = $this->createBook('Carrie', 'Stephen King');
        $this->bookRepository->add($book);

        $savedBook = $this->bookRepository->findOneBy(['title' => 'Carrie']);
        $this->assertInstanceOf(Book::class, $savedBook);
        $this->assertBookEquals($savedBook, 'Carrie', 'Stephen King');
    }

    public function testFindOneByAuthor(): void
    {
        $book = $this->createBook('The Eagle Has Landed', 'Jack Higgins');
        $this->bookRepository->add($book);

        $savedBook = $this->bookRepository->findOneBy(['author' => 'Jack Higgins']);
        $this->assertInstanceOf(Book::class, $savedBook);
        $this->assertBookEquals($savedBook, 'The Eagle Has Landed', 'Jack Higgins');
    }

    public function testAddOne(): void
    {
        $book = $this->createBook('The Martian', 'Andy Weir');
        $this->bookRepository->add($book);

        $savedBook = $this->bookRepository->findOneBy(['id' => $book->getId()]);
        $this->assertBookEquals($savedBook, 'The Martian', 'Andy Weir');
    }

    public function testRemoveOne(): void
    {
        $book = $this->createBook('Carrie', 'Stephen King');
        $this->bookRepository->add($book);

        $book = $this->bookRepository->findOneBy(['title' => 'Carrie']);
        $this->bookRepository->remove($book);

        $removedBook = $this->bookRepository->findOneBy(['title' => 'Carrie']);
        $this->assertNull($removedBook);
    }

    private function createBook(string $title, string  $author): Book
    {
        $book = new Book();
        $book->setTitle($title);
        $book->setAuthor($author);
        return $book;
    }

    private function assertBookEquals(Book $book, string $expectedTitle, string $expectedAuthor): void
    {
        $this->assertInstanceOf(Book::class, $book);
        $this->assertEquals($expectedTitle, $book->getTitle());
        $this->assertEquals($expectedAuthor, $book->getAuthor());
    }

}
