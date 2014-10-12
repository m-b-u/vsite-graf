#define M 20
#define N 10

// N rows, M columns

#import <iostream>

using namespace std;

/* Bad practice, hardcoding dimensions of arrays. For 1D, use std::array, but I don't 
   want to put emphasis on C++ native array vs. array class here.
*/


void clear_framebuffer( unsigned char (&A)[N][M] ) {
/* Fills the entire framebuffer of width M, and height N with zeros.
   N and M are not real parameters here! They are global constants
   (technically, not even that - just literals)
*/
  for (unsigned i = 0; i < N; ++i) {
    for (unsigned j = 0; j < M; ++j) {
      A[i][j] = '.';  // dot is our 0 or black, for a bit nicer output.
    }
  }
}

void clear_framebuffer_1D( unsigned char *A_, unsigned n, unsigned m) 
/* be sure to pass correct dimensions, otherwise - buffer overflow.
   Better yet, use some sane container
*/
{
  unsigned len = n*m;
  for (unsigned i = 0; i < len; ++i, ++A_) 
    *A_ = '.'; // bit faster than doing A_[i] all the time. Why?
}


void print_framebuffer( unsigned char (&A)[N][M] )
{
  cout << endl << '+';
  for (unsigned j = 0; j < M; ++j) 
    cout << '-';
  cout << '+' << endl;
  for (unsigned i = 0; i < N; ++i) {
    cout << '|';
    for (unsigned j = 0; j < M; ++j) {
      cout << A[i][j];
    }
    cout << '|' << endl;
  }
  cout << '+';
  for (unsigned j = 0; j < M; ++j) 
    cout << '-';
  cout << '+' << endl;
}  

int main (void)
{
  unsigned char A[N][M];
  clear_framebuffer (A);
  A[2][5] = '*'; // Third row, sixth column (we count from 0)

  print_framebuffer(A);

  unsigned char *A_ = reinterpret_cast<unsigned char *>(A); 
  /* Now we take this memory space as the 1D array, as is already is internaly.
     Just the compiled code handles multiplications and additons instead of us.
  */

  A_[2*M + 5] = '@'; // replace the asterisk with monkey

  print_framebuffer(A);
  
  // Check the result
}

