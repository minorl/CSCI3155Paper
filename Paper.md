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



Motivation: Why do people want this?

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
