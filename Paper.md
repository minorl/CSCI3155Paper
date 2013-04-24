Introduction (purpose: power of community discussion and cocain:

Scala did not originally include the withFilter class in its early implementations.  It was instead added in version 2.8 as a result of community discussion to address the particulars of filter and how guards with side effects work.  This discourse highlights a popular approach in the open source community to identify problems, discuss new ideas, and design functionality using direct feedback from users and other developers.  Martin Odersky communicated with the scala community through a mailing list to address open tickets requesting new for-expression behaviors.  The subsequent discussion resulted in the addition of a new class called withFilter.  At first glance, it may appear that withFilter and filter are identical due to the syntax and situations in which they are used.  Understanding the motivations and implementations of the two methods highlights the benefits of an open source community driven language.  

Motivation:
According to a post by Martin Odersky, the main motivations for expanding filter are:
(1) you might want to write a guard that depends on side effects in body.
(2) you might want to avoid constructing a secondary list or other
data structure containing the filtered elements.
<citation>
The first motivation is explained further using the following example code and output:

 var limit = 2
 for (i <- List(0, 1, 2, 3) if i <= limit; j <- 0 until limit) yield
{ limit = 4; (i, j) }

What does it return?

 List((0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3))
<citation>

From this simple example we see that one of the indices captures the value of ‘limit’ before it is changed and the second captures the value of ‘limit’ after it is changed in the body.  This behavior is, to say it nicely, non-intuitive.  The second motivation is one of performance.  Consider a case where a programmer chains filter with another iterative function such as Map.  In this case the transversable object would be iterated over two times.  Now consider if more more and more chains of functions were used.  With every function that gets chained, the input needs to be traversed once again.  A more efficient implementation would only need to traverse the input a single time applying each of the chained functions to a single element as it iterates.  With these two reasons in mind, Ordersky formed the ORTHOGONAL basis a new set of functions.  His original idea was to write filterMap, filterFlatMap, and filterForeach.  This idea was reformulated into a single function; withFilter.

Because filter will apply itself to an entire list and return a sublist and WithFilter will apply on an element by element basis if it is called by another function. The functionality of withfilter over filter is that withFilter can use side effects from the body of a for statement to alter the guard. The example code below? shows how filter is applied to the entirety of an immutable list, and how withFilter can be applied element by element when called by iterative functions. When applied to transversable elements, this changes the monadic interpretations of -for- statements in the Scala language.
Implementation:
The actual implementation of filter is simply a for-yield statement that iterates through an entire transversable object. It uses the function that the filter is applying in the body of the for-yield statement to return a transversable object. This shows the "strictness" of filter eg the entire object is traversed before any other operation may be applied to the input. On the other hand, the implementation of withFilter is not a for-yield statement. Instead it is implemented on the idea that another method can be applied simultaneously such as map, flatmap, foreach, or even another withfilter. With this in mind withFilter applies the operation that follows as it applies the filtering function. The result of these two implementations is that when chained with map, flatmap, etc. filter will apply these post hoc while withFilter will apply them as the transversable object is iterated.
Rejected ideas: What were some other solutions?
Accepted idea: Why was withFilter accepted when other things weren't?
Implementation: Maybe go into the implementation, uses flat map so this is relevent. Also, maybe check to see if it has been changed in more recent revisions

Conclusions:
Citations:
