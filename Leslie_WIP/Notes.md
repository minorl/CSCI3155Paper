Group:
======================

Ken Garry

Erik Kierstead

Leslie Minor

Topic:
======================

Scala string interpolation, allowing for variables in strings ($ to escape) and formatting flags (%). Things of interest can include the implications because the Java representation of strings are immutable or something like that. 

Code Example:
======================

Before the SIP:

    “Bob is “+n+” years old” 

After the SIP:

    s“Bob is $n years old”


Resources:
======================

[SIP11:]{https://docs.google.com/document/d/1NdxNxZYodPA-c4MLr33KzwzKFkzm9iW9POexT9PkJsU/edit?hl=en_US#}

[SIP-11 String Interpolation - not for raw String?]{https://groups.google.com/forum/?fromgroups=#!searchin/scala-sips/SIP$2011/scala-sips/RB8j2P1ndto/oVKm-eQcH2cJ}

[SIP-11 too broken to ship as-is, IMO]{https://groups.google.com/forum/?fromgroups=#!topic/scala-sips/xytEbiIVfyc}

[SIP-11 New version of string interpolation proposal]{https://groups.google.com/forum/?fromgroups=#!topic/scala-sips/vKYKE6SMUEk}

[SIP 11 Alternative string interpolation proposal]{https://groups.google.com/forum/?fromgroups=#!topic/scala-sips/oFHvNHi7eB8}
