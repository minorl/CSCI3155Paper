##Birth of withFilter


####What is it?!

Primarily, what is the difference between filter and withFilter? Let's first examine both with regards to list. From the Scala API: "Note: the difference between c filter p and c withFilter p is that the former creates a new collection, whereas the latter only restricts the domain of subsequent map, flatMap, foreach, and withFilter operations." [Scala API - List][]

<!--- def filter(p: (A) ⇒ Boolean): List[A]
Selects all elements of this list which satisfy a predicate.
p    the predicate used to test elements.
returns    a new list consisting of all elements of this list that satisfy the given predicate p. The order of the elements is preserved.

def withFilter(p: (A) ⇒ Boolean): FilterMonadic[A, List[A]]
Creates a non-strict filter of this list.

Note: the difference between c filter p and c withFilter p is that the former creates a new collection, whereas the latter only restricts the domain of subsequent map, flatMap, foreach, and withFilter operations.
p    the predicate used to test elements.
returns    an object of class WithFilter, which supports map, flatMap, foreach, and withFilter operations. All these operations apply to those elements of this list which satisfy the predicate p.
--->


```scala
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

```

#Erik's Stuff

Users new to Scala are often confused by the many nuances inherent in functional programming. Complicated expressions and datatypes in analogous imperative languages are reduced to mere lines of code, the mechanics of which lie hidden behind the elegance of recursive statements with functions as values. The filter and withFilter classes are ideal examples of this high-level abstraction. Their respective implementations appear essentially identical, and both will produce the same results.

--figure-- --figure--

Scala did not originally include the class withFilter but instead was added as a result of community discussion (cite sources). It offers performance benifits over filter under certain circumstances, extends a different class in the type hierarchy (cite scala-lang.org), and even returns a different value type. These characteristics first appear counter-intuitive, given how similiar their code is to use in practice. In highlighting the differences between the classes the question is not what the filters are doing, or when they are used, but in how the are implemented.

Filter extends the transformer class and works by applying some conditional over all elements of a list. This conditional can come in a variety of flavors, from simple comparison statements to complicated functions. Applying multiple filters to a list causes a chaining process which requires the list to be iterated over per-filter. This results in a complexity of n^m, where n is the size of the list and m is the filter total (cite source). As lists become large, and the chaining becomes verbose, there is potentially a very costly computation associated with use of the filter class.

withFilter differs very subtley from its counterpart by a change in its return type. Like filter, it applies a conditional over a list, but cannot traverse a list by itself to perform that filtering. Instead, withFilter requires a map, flatmap, or foreach statement to act on its return value. (more apply?) When this statement then iterates over the list the withFilter gets applied to each element as it does. This is an enormous boon to performance, as it ensures that the list is traversed only once, no matter how complex of a filter is used.

--output samples-- scala> testlist.withFilter(x => (x%2 == 0 )).map(x => x) res3: List[Int] = List(10, 20, 30, 50)

scala> testlist.withFilter(x => (x%2 == 0 )) res4: scala.collection.generic.FilterMonadic[Int,List[Int]] = scala.collection.TraversableLike$WithFilter@257db177

scala> testlist.filter(x => (x%2 == 0 )).map(x => x) res5: List[Int] = List(10, 20, 30, 50)

scala> testlist.filter(x => (x%2 == 0 )) res6: List[Int] = List(10, 20, 30, 50) --output samples--

PS: I'm not sure what benefit this really has with respect to guards. MOAR RESEARCH NEEDED <3

Motivation:

The filter function will apply itself to an entire list and return a sublist. WithFilter will apply on an element by element basis if it is called by another function. The functionality of withfilter over filter is that withFilter can use side effects from the body of a for statement to alter the guard. The example code below? shows how filter is applied to the entirety of an immutable list, and how withFilter can be applied element by element when called by iterative functions. When applied to transversable elments, this changes the monadic interpretations of -for- statements in the Scala language.

Rejected ideas: What were some other solutions?

Accepted idea: Why was withFilter accepted when other things weren't?

Implementation: Maybe go into the implementation, uses flat map so this is relevent. Also, maybe check to see if it has been changed in more recent revisions


Resources:
=========================

[Motivation and discussion][] Mailing list discussion resulting in withFilter

[Implementation][] Code revision with newly implemented withFilter

[Example with for][] Excellent example from stackoverflow (wtf it duz)

[General example][] Uses little words, tries to explain the differences. 


[Motivation and discussion]:http://scala-programming-language.1934581.n4.nabble.com/Rethinking-filter-td2009215.html

[Example with for]: http://stackoverflow.com/a/1059501

[General example]: http://tataryn.net/2011/10/whats-in-a-scala-for-comprehension/

[Implementation]:https://code.google.com/p/scalacheck/source/diff?spec=svn506&r=506&format=side&path=/trunk/src/main/scala/org/scalacheck/Gen.scala

[Scala API - List]: http://www.scala-lang.org/api/current/index.html#scala.collection.immutable.List
