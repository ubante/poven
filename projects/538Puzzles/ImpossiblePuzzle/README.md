This is from http://fivethirtyeight.com/features/can-you-solve-the-impossible-puzzle/

# Problem definition

Three very skilled logicians are sitting around a table — Barack, Pete and Susan. Barack says: 
“I’m thinking of two natural numbers between 1 and 9, inclusive. I’ve written the product of these 
two numbers on this paper that I’m giving to you, Pete. I’ve written the sum of the two numbers on 
this paper that I’m giving to you, Susan. Now Pete, looking at your paper, do you know which 
numbers I’m thinking of?”

Pete looks at his paper and says: “No, I don’t.”

Barack turns to Susan and asks: “Susan, do you know which numbers I’m thinking of?” Susan looks at 
her paper and says: “No.”

Barack turns back to Pete and asks: “How about now? Do you know?”

“No, I still don’t,” Pete says.

Barack keeps going back and forth, and when he asks Pete for the fifth time, Pete says: “Yes, now 
I know!”

First, what are the two numbers? Second, if Pete had said no the fifth time, would Susan have said 
yes or no at her fifth turn?

# Solution
Answer description:
First, you find the 45 different products of A and B where A>=B.  We can ignore the A<B cases 
because of symmetry.  Putting this in a matrix helps.

Then you find the products that occur just once.  If the number Pete is given occurs just once, 
then he knows Barack's two numbers.  But Pete says no.  Remove those numbers from the matrix.

Susan then replaces all the remaining products in the matrix with sums.  If the number she was 
given occurs exactly once, then she knows Barack's two numbers. But Susan says no so remove those 
numbers from the Matrix. 