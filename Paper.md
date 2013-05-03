Scala did not originally include the withFilter method in its early implementations.  It was instead added in version 2.8 as a result of community discussion to address issues with filter and for expressions.  This discourse highlights a popular approach in the open source community to identify problems, discuss new ideas, and design functionality using direct feedback from users and other developers.  Martin Odersky communicated with the scala community through a mailing list to address open tickets requesting new for-expression behaviors.  The discussion that followed resulted in the addition of a new method called withFilter.  At first glance, it may appear that withFilter and filter are identical due to the syntax and situations in which they are used.  Understanding the motivations and implementations of the two methods highlights the benefits of an open source community driven language.  

According to a post by Martin Odersky, the main motivations for rethinking filter are: you might want to write a guard that depends on side effects in body; you might want to avoid constructing a secondary list or other data structure containing the filtered elements.
The first motivation is explained further using the following example code and output (from pre 2.8 scala):

    var limit = 2
    for (i <- List(0, 1, 2, 3) if i <= limit; j <- 0 until limit) yield { limit = 4; (i, j) }


What does it return?

    List((0,0), (0,1), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3))


From this simple example we see that one of the indices captures the value of ‘limit’ before it is changed and the second captures the value of ‘limit’ after it is changed in the body.  This behavior is, to say it nicely, non-intuitive.  

The second motivation is one of performance.  Consider a case where a programmer chains filter with another iterative function such as Map.  In this case the transversable object would be iterated over two times.  Now consider if more more and more chains of functions were used.  With every function that gets chained, the input needs to be traversed once again.  A more efficient implementation would only need to traverse the input a single time applying each of the chained functions to a single element as it iterates.  With these two reasons in mind, Ordersky formed the basis of a new set of functions.  His original idea was to write filterMap, filterFlatMap, and filterForeach.  This idea was later reformulated into a single function; withFilter.
Because filter will apply itself to an entire list and return a sublist and withFilter will apply on an element by element basis if it is called by another function. The functionality of withFilter over filter is that withFilter can use side effects from the body of a for statement to alter the guard. The example code below shows how filter is applied to the entirety of an immutable list, and how withFilter can be applied element by element when called by iterative functions. When applied to transversable elements, this changes the monadic interpretations of -for- statements in the Scala language.

Example code and output:

    scala> var found = false
    found: Boolean = false
    scala> List.range(1,10).filter(_ % 2 == 1 && !found).foreach(x => if (x == 5) found = true else println(x))
    1
    3
    7
    9

    scala> found = false
    found: Boolean = false
    scala> List.range(1,10).withFilter(_ % 2 == 1 && !found).foreach(x => if (x == 5) found = true else println(x))
    1
    3

When the idea of a change to the filter method was first suggested, the Scala community reacted both positively and negatively. When Martin Odersky first proposed changes to how for-yield behaved he was met with both support and resistance from the mailing list.  His suggestion to resolve the open tickets revolved around where to place the guard within the for-expression and the impact that this change would have on the for-yield expression.  In making this change, and ensuring for-yield still performed as expected, additional methods filterForeach, filterMap, filterFlatMap would be added inside the generator classes.  Responses to this suggestion were mixed.

On the positive side the initial suggested implementation would improve performance characteristics for chaining filter with other methods, make for expressions more powerful, and act more intuitively for imperative users.  In favor of the suggestion was user Eastsun, who replied “I'm looking for this so long time.” 

On the negative side, the community was concerned that it would unnecessarily complicate the Scala source code, break existing code, and there was existing framework in place to overcome problems being addressed. Jesper Nordenberg replied “Regarding the yield-case, the only motivation I can see is performance, but it's not worth complicating the rewrite rules for that. It's better to put more work into the optimizer in that case.” 

However, after the final implementation was revealed by Martin Odersky, the community reaction was overwhelmingly positive. As Daniel Sobral said, “I like this much better than the previous proposals. It doesn't change "filter" in unexpected ways, makes guards more intuitive, it is rather simple and has performance benefits.”

The actual implementation of filter is simply a for-yield statement that iterates through an entire transversable object. It uses the function that the filter is applying in the body of the for-yield statement to return a transversable object. This shows the "strictness" of filter eg the entire object is traversed before any other operation may be applied to the input. On the other hand, the implementation of withFilter is not a for-yield statement. Instead it is implemented on the idea that another method can be applied simultaneously such as map, flatmap, foreach, or even another withfilter. With this in mind withFilter applies the operation that follows as it applies the filtering function. The result of these two implementations is that when chained with map, flatmap, etc. filter will apply these post hoc while withFilter will apply them as the transversable object is iterated.

The only thing left to consider was how the method would be introduced. The proposed implementation would be included in the Scala 2.8 release and would assure backwards compatibility for existing code.  Backwards compatibility would be ensured by simply replacing withFilter with filter when the compiler could not find the withFilter method, and a depreciation warning would be thrown.

Open source communities like Scala can thrive largely in part due to the direct conversations that exist between developers and the users.  The genesis of withFilter serves as an example which highlights the ideal results of such dialogues.  Intended changes to filter were reviewed and discussed by the community allowing feedback without the labor required for execution.  Within 24 hours a new method was proposed, born from the mind of Odersky.  This withFilter enhanced performance for multiple filters, allowed for backwards compatibility, and was heralded as a creative triumph by the community at large.  Without developers having an open door policy with the people their products serve such successes as withFilter may never have been created.  



--------

Resources:
=========================

[Motivation and discussion][] Mailing list discussion resulting in withFilter

[Implementation][] Code revision with newly implemented withFilter

[Example with for][] Excellent example from stackoverflow

[General example][] Uses little words, tries to explain the differences. 


[Motivation and discussion]:http://scala-programming-language.1934581.n4.nabble.com/Rethinking-filter-td2009215.html

[Example with for]: http://stackoverflow.com/a/1059501

[General example]: http://tataryn.net/2011/10/whats-in-a-scala-for-comprehension/

[Implementation]:https://code.google.com/p/scalacheck/source/diff?spec=svn506&r=506&format=side&path=/trunk/src/main/scala/org/scalacheck/Gen.scala
