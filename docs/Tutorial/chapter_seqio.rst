Sequence Input/Output
=====================

In this chapter we’ll discuss in more detail the ``Bio.SeqIO`` module,
which was briefly introduced in Chapter [chapter:quick-start] and also
used in Chapter [chapter:SeqRecord]. This aims to provide a simple
interface for working with assorted sequence file formats in a uniform
way. See also the ``Bio.SeqIO`` wiki page
(http://biopython.org/wiki/SeqIO), and the built in documentation (also
`online <http://biopython.org/DIST/docs/api/Bio.SeqIO-module.html>`__):

::

    >>> from Bio import SeqIO
    >>> help(SeqIO)
    ...

The “catch” is that you have to work with ``SeqRecord`` objects (see
Chapter [chapter:SeqRecord]), which contain a ``Seq`` object (see
Chapter [chapter:Bio.Seq]) plus annotation like an identifier and
description. Note that when dealing with very large FASTA or FASTQ
files, the overhead of working with all these objects can make scripts
too slow. In this case consider the low-level ``SimpleFastaParser`` and
``FastqGeneralIterator`` parsers which return just a tuple of strings
for each record (see Section [sec:low-level-fasta-fastq]).

Parsing or Reading Sequences
----------------------------

The workhorse function ``Bio.SeqIO.parse()`` is used to read in sequence
data as SeqRecord objects. This function expects two arguments:

#. The first argument is a *handle* to read the data from, or a
   filename. A handle is typically a file opened for reading, but could
   be the output from a command line program, or data downloaded from
   the internet (see Section [sec:SeqIO\_Online]). See
   Section [sec:appendix-handles] for more about handles.

#. The second argument is a lower case string specifying sequence format
   – we don’t try and guess the file format for you! See
   http://biopython.org/wiki/SeqIO for a full listing of supported
   formats.

There is an optional argument ``alphabet`` to specify the alphabet to be
used. This is useful for file formats like FASTA where otherwise
``Bio.SeqIO`` will default to a generic alphabet.

The ``Bio.SeqIO.parse()`` function returns an *iterator* which gives
``SeqRecord`` objects. Iterators are typically used in a for loop as
shown below.

Sometimes you’ll find yourself dealing with files which contain only a
single record. For this situation use the function ``Bio.SeqIO.read()``
which takes the same arguments. Provided there is one and only one
record in the file, this is returned as a ``SeqRecord`` object.
Otherwise an exception is raised.

Reading Sequence Files
~~~~~~~~~~~~~~~~~~~~~~

In general ``Bio.SeqIO.parse()`` is used to read in sequence files as
``SeqRecord`` objects, and is typically used with a for loop like this:

::

    from Bio import SeqIO
    for seq_record in SeqIO.parse("ls_orchid.fasta", "fasta"):
        print(seq_record.id)
        print(repr(seq_record.seq))
        print(len(seq_record))

The above example is repeated from the introduction in
Section [sec:sequence-parsing], and will load the orchid DNA sequences
in the FASTA format file
`ls\_orchid.fasta <https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.fasta>`__.
If instead you wanted to load a GenBank format file like
`ls\_orchid.gbk <https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.gbk>`__
then all you need to do is change the filename and the format string:

::

    from Bio import SeqIO
    for seq_record in SeqIO.parse("ls_orchid.gbk", "genbank"):
        print(seq_record.id)
        print(repr(seq_record.seq))
        print(len(seq_record))

Similarly, if you wanted to read in a file in another file format, then
assuming ``Bio.SeqIO.parse()`` supports it you would just need to change
the format string as appropriate, for example “swiss” for SwissProt
files or “embl” for EMBL text files. There is a full listing on the wiki
page (http://biopython.org/wiki/SeqIO) and in the built in documentation
(also
`online <http://biopython.org/DIST/docs/api/Bio.SeqIO-module.html>`__).

Another very common way to use a Python iterator is within a list
comprehension (or a generator expression). For example, if all you
wanted to extract from the file was a list of the record identifiers we
can easily do this with the following list comprehension:

::

    >>> from Bio import SeqIO
    >>> identifiers = [seq_record.id for seq_record in SeqIO.parse("ls_orchid.gbk", "genbank")]
    >>> identifiers
    ['Z78533.1', 'Z78532.1', 'Z78531.1', 'Z78530.1', 'Z78529.1', 'Z78527.1', ..., 'Z78439.1']

There are more examples using ``SeqIO.parse()`` in a list comprehension
like this in Section [seq:sequence-parsing-plus-pylab] (e.g. for
plotting sequence lengths or GC%).

Iterating over the records in a sequence file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the above examples, we have usually used a for loop to iterate over
all the records one by one. You can use the for loop with all sorts of
Python objects (including lists, tuples and strings) which support the
iteration interface.

The object returned by ``Bio.SeqIO`` is actually an iterator which
returns ``SeqRecord`` objects. You get to see each record in turn, but
once and only once. The plus point is that an iterator can save you
memory when dealing with large files.

Instead of using a for loop, can also use the ``next()`` function on an
iterator to step through the entries, like this:

::

    from Bio import SeqIO
    record_iterator = SeqIO.parse("ls_orchid.fasta", "fasta")

    first_record = next(record_iterator)
    print(first_record.id)
    print(first_record.description)

    second_record = next(record_iterator)
    print(second_record.id)
    print(second_record.description)

Note that if you try to use ``next()`` and there are no more results,
you’ll get the special ``StopIteration`` exception.

One special case to consider is when your sequence files have multiple
records, but you only want the first one. In this situation the
following code is very concise:

::

    from Bio import SeqIO
    first_record = next(SeqIO.parse("ls_orchid.gbk", "genbank"))

A word of warning here – using the ``next()`` function like this will
silently ignore any additional records in the file. If your files have
*one and only one* record, like some of the online examples later in
this chapter, or a GenBank file for a single chromosome, then use the
new ``Bio.SeqIO.read()`` function instead. This will check there are no
extra unexpected records present.

Getting a list of the records in a sequence file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the previous section we talked about the fact that
``Bio.SeqIO.parse()`` gives you a ``SeqRecord`` iterator, and that you
get the records one by one. Very often you need to be able to access the
records in any order. The Python ``list`` data type is perfect for this,
and we can turn the record iterator into a list of ``SeqRecord`` objects
using the built-in Python function ``list()`` like so:

::

    from Bio import SeqIO
    records = list(SeqIO.parse("ls_orchid.gbk", "genbank"))

    print("Found %i records" % len(records))

    print("The last record")
    last_record = records[-1] #using Python's list tricks
    print(last_record.id)
    print(repr(last_record.seq))
    print(len(last_record))

    print("The first record")
    first_record = records[0] #remember, Python counts from zero
    print(first_record.id)
    print(repr(first_record.seq))
    print(len(first_record))

Giving:

::

    Found 94 records
    The last record
    Z78439.1
    Seq('CATTGTTGAGATCACATAATAATTGATCGAGTTAATCTGGAGGATCTGTTTACT...GCC', IUPACAmbiguousDNA())
    592
    The first record
    Z78533.1
    Seq('CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGG...CGC', IUPACAmbiguousDNA())
    740

You can of course still use a for loop with a list of ``SeqRecord``
objects. Using a list is much more flexible than an iterator (for
example, you can determine the number of records from the length of the
list), but does need more memory because it will hold all the records in
memory at once.

Extracting data
~~~~~~~~~~~~~~~

The ``SeqRecord`` object and its annotation structures are described
more fully in Chapter [chapter:SeqRecord]. As an example of how
annotations are stored, we’ll look at the output from parsing the first
record in the GenBank file
`ls\_orchid.gbk <https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.gbk>`__.

::

    from Bio import SeqIO
    record_iterator = SeqIO.parse("ls_orchid.gbk", "genbank")
    first_record = next(record_iterator)
    print(first_record)

That should give something like this:

::

    ID: Z78533.1
    Name: Z78533
    Description: C.irapeanum 5.8S rRNA gene and ITS1 and ITS2 DNA.
    Number of features: 5
    /sequence_version=1
    /source=Cypripedium irapeanum
    /taxonomy=['Eukaryota', 'Viridiplantae', 'Streptophyta', ..., 'Cypripedium']
    /keywords=['5.8S ribosomal RNA', '5.8S rRNA gene', ..., 'ITS1', 'ITS2']
    /references=[...]
    /accessions=['Z78533']
    /data_file_division=PLN
    /date=30-NOV-2006
    /organism=Cypripedium irapeanum
    /gi=2765658
    Seq('CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGG...CGC', IUPACAmbiguousDNA())

This gives a human readable summary of most of the annotation data for
the ``SeqRecord``. For this example we’re going to use the
``.annotations`` attribute which is just a Python dictionary. The
contents of this annotations dictionary were shown when we printed the
record above. You can also print them out directly:

::

    print(first_record.annotations)

Like any Python dictionary, you can easily get a list of the keys:

::

    print(first_record.annotations.keys())

or values:

::

    print(first_record.annotations.values())

In general, the annotation values are strings, or lists of strings. One
special case is any references in the file get stored as reference
objects.

Suppose you wanted to extract a list of the species from the
`ls\_orchid.gbk <https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.gbk>`__
GenBank file. The information we want, *Cypripedium irapeanum*, is held
in the annotations dictionary under ‘source’ and ‘organism’, which we
can access like this:

::

    >>> print(first_record.annotations["source"])
    Cypripedium irapeanum

or:

::

    >>> print(first_record.annotations["organism"])
    Cypripedium irapeanum

In general, ‘organism’ is used for the scientific name (in Latin, e.g.
*Arabidopsis thaliana*), while ‘source’ will often be the common name
(e.g. thale cress). In this example, as is often the case, the two
fields are identical.

Now let’s go through all the records, building up a list of the species
each orchid sequence is from:

::

    from Bio import SeqIO
    all_species = []
    for seq_record in SeqIO.parse("ls_orchid.gbk", "genbank"):
        all_species.append(seq_record.annotations["organism"])
    print(all_species)

Another way of writing this code is to use a list comprehension:

::

    from Bio import SeqIO
    all_species = [seq_record.annotations["organism"] for seq_record in \
                   SeqIO.parse("ls_orchid.gbk", "genbank")]
    print(all_species)

In either case, the result is:

::

    ['Cypripedium irapeanum', 'Cypripedium californicum', ..., 'Paphiopedilum barbatum']

Great. That was pretty easy because GenBank files are annotated in a
standardised way.

Now, let’s suppose you wanted to extract a list of the species from a
FASTA file, rather than the GenBank file. The bad news is you will have
to write some code to extract the data you want from the record’s
description line - if the information is in the file in the first place!
Our example FASTA format file
`ls\_orchid.fasta <https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.fasta>`__
starts like this:

::

    >gi|2765658|emb|Z78533.1|CIZ78533 C.irapeanum 5.8S rRNA gene and ITS1 and ITS2 DNA
    CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGATGAGACCGTGGAATAAACGATCGAGTG
    AATCCGGAGGACCGGTGTACTCAGCTCACCGGGGGCATTGCTCCCGTGGTGACCCTGATTTGTTGTTGGG
    ...

You can check by hand, but for every record the species name is in the
description line as the second word. This means if we break up each
record’s ``.description`` at the spaces, then the species is there as
field number one (field zero is the record identifier). That means we
can do this:

::

    from Bio import SeqIO
    all_species = []
    for seq_record in SeqIO.parse("ls_orchid.fasta", "fasta"):
        all_species.append(seq_record.description.split()[1])
    print(all_species)

This gives:

::

    ['C.irapeanum', 'C.californicum', 'C.fasciculatum', 'C.margaritaceum', ..., 'P.barbatum']

The concise alternative using list comprehensions would be:

::

    from Bio import SeqIO
    all_species == [seq_record.description.split()[1] for seq_record in \
                    SeqIO.parse("ls_orchid.fasta", "fasta")]
    print(all_species)

In general, extracting information from the FASTA description line is
not very nice. If you can get your sequences in a well annotated file
format like GenBank or EMBL, then this sort of annotation information is
much easier to deal with.

Parsing sequences from compressed files
---------------------------------------

In the previous section, we looked at parsing sequence data from a file.
Instead of using a filename, you can give ``Bio.SeqIO`` a handle (see
Section [sec:appendix-handles]), and in this section we’ll use handles
to parse sequence from compressed files.

As you’ll have seen above, we can use ``Bio.SeqIO.read()`` or
``Bio.SeqIO.parse()`` with a filename - for instance this quick example
calculates the total length of the sequences in a multiple record
GenBank file using a generator expression:

::

    >>> from Bio import SeqIO
    >>> print(sum(len(r) for r in SeqIO.parse("ls_orchid.gbk", "gb")))
    67518

Here we use a file handle instead, using the ``with`` statement to close
the handle automatically:

::

    >>> from Bio import SeqIO
    >>> with open("ls_orchid.gbk") as handle:
    ...     print(sum(len(r) for r in SeqIO.parse(handle, "gb")))
    67518

Or, the old fashioned way where you manually close the handle:

::

    >>> from Bio import SeqIO
    >>> handle = open("ls_orchid.gbk")
    >>> print(sum(len(r) for r in SeqIO.parse(handle, "gb")))
    67518
    >>> handle.close()

Now, suppose we have a gzip compressed file instead? These are very
commonly used on Linux. We can use Python’s ``gzip`` module to open the
compressed file for reading - which gives us a handle object:

::

    >>> import gzip
    >>> from Bio import SeqIO
    >>> with gzip.open("ls_orchid.gbk.gz", "rt") as handle:
    ...     print(sum(len(r) for r in SeqIO.parse(handle, "gb")))
    ...
    67518

Similarly if we had a bzip2 compressed file (sadly the function name
isn’t quite as consistent under Python 2):

::

    >>> import bz2
    >>> from Bio import SeqIO
    >>> if hasattr(bz2, "open"):
    ...     handle = bz2.open("ls_orchid.gbk.bz2", "rt")  # Python 3
    ... else:
    ...     handle = bz2.BZ2File("ls_orchid.gbk.bz2", "r")  # Python 2
    ...
    >>> with handle:
    ...     print(sum(len(r) for r in SeqIO.parse(handle, "gb")))
    ...
    67518

There is a gzip (GNU Zip) variant called BGZF (Blocked GNU Zip Format),
which can be treated like an ordinary gzip file for reading, but has
advantages for random access later which we’ll talk about later in
Section [sec:SeqIO-index-bgzf].

Parsing sequences from the net
------------------------------

In the previous sections, we looked at parsing sequence data from a file
(using a filename or handle), and from compressed files (using a
handle). Here we’ll use ``Bio.SeqIO`` with another type of handle, a
network connection, to download and parse sequences from the internet.

Note that just because you *can* download sequence data and parse it
into a ``SeqRecord`` object in one go doesn’t mean this is a good idea.
In general, you should probably download sequences *once* and save them
to a file for reuse.

Parsing GenBank records from the net
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Section [sec:efetch] talks about the Entrez EFetch interface in more
detail, but for now let’s just connect to the NCBI and get a few
*Opuntia* (prickly-pear) sequences from GenBank using their GI numbers.

First of all, let’s fetch just one record. If you don’t care about the
annotations and features downloading a FASTA file is a good choice as
these are compact. Now remember, when you expect the handle to contain
one and only one record, use the ``Bio.SeqIO.read()`` function:

::

    from Bio import Entrez
    from Bio import SeqIO
    Entrez.email = "A.N.Other@example.com"
    with Entrez.efetch(db="nucleotide", rettype="fasta", retmode="text", id="6273291") as handle:
        seq_record = SeqIO.read(handle, "fasta")
    print("%s with %i features" % (seq_record.id, len(seq_record.features)))

Expected output:

::

    gi|6273291|gb|AF191665.1|AF191665 with 0 features

The NCBI will also let you ask for the file in other formats, in
particular as a GenBank file. Until Easter 2009, the Entrez EFetch API
let you use “genbank” as the return type, however the NCBI now insist on
using the official return types of “gb” (or “gp” for proteins) as
described on `EFetch for Sequence and other Molecular Biology
Databases <https://www.ncbi.nlm.nih.gov/books/NBK3837/>`__. As a result,
in Biopython 1.50 onwards, we support “gb” as an alias for “genbank” in
``Bio.SeqIO``.

::

    from Bio import Entrez
    from Bio import SeqIO
    Entrez.email = "A.N.Other@example.com"
    with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id="6273291") as handle
        seq_record = SeqIO.read(handle, "gb") #using "gb" as an alias for "genbank"
    print("%s with %i features" % (seq_record.id, len(seq_record.features)))

The expected output of this example is:

::

    AF191665.1 with 3 features

Notice this time we have three features.

Now let’s fetch several records. This time the handle contains multiple
records, so we must use the ``Bio.SeqIO.parse()`` function:

::

    from Bio import Entrez
    from Bio import SeqIO
    Entrez.email = "A.N.Other@example.com"
    with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",
                       id="6273291,6273290,6273289") as handle:
        for seq_record in SeqIO.parse(handle, "gb"):
            print("%s %s..." % (seq_record.id, seq_record.description[:50]))
            print("Sequence length %i, %i features, from: %s"
                  % (len(seq_record), len(seq_record.features), seq_record.annotations["source"]))

That should give the following output:

::

    AF191665.1 Opuntia marenae rpl16 gene; chloroplast gene for c...
    Sequence length 902, 3 features, from: chloroplast Opuntia marenae
    AF191664.1 Opuntia clavata rpl16 gene; chloroplast gene for c...
    Sequence length 899, 3 features, from: chloroplast Grusonia clavata
    AF191663.1 Opuntia bradtiana rpl16 gene; chloroplast gene for...
    Sequence length 899, 3 features, from: chloroplast Opuntia bradtianaa

See Chapter [chapter:entrez] for more about the ``Bio.Entrez`` module,
and make sure to read about the NCBI guidelines for using Entrez
(Section [sec:entrez-guidelines]).

Parsing SwissProt sequences from the net
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now let’s use a handle to download a SwissProt file from ExPASy,
something covered in more depth in Chapter [chapter:swiss\_prot]. As
mentioned above, when you expect the handle to contain one and only one
record, use the ``Bio.SeqIO.read()`` function:

::

    from Bio import ExPASy
    from Bio import SeqIO
    with ExPASy.get_sprot_raw("O23729") as handle:
        seq_record = SeqIO.read(handle, "swiss")
    print(seq_record.id)
    print(seq_record.name)
    print(seq_record.description)
    print(repr(seq_record.seq))
    print("Length %i" % len(seq_record))
    print(seq_record.annotations["keywords"])

Assuming your network connection is OK, you should get back:

::

    O23729
    CHS3_BROFI
    RecName: Full=Chalcone synthase 3; EC=2.3.1.74; AltName: Full=Naringenin-chalcone synthase 3;
    Seq('MAPAMEEIRQAQRAEGPAAVLAIGTSTPPNALYQADYPDYYFRITKSEHLTELK...GAE', ProteinAlphabet())
    Length 394
    ['Acyltransferase', 'Flavonoid biosynthesis', 'Transferase']

Sequence files as Dictionaries
------------------------------

We’re now going to introduce three related functions in the
``Bio.SeqIO`` module which allow dictionary like random access to a
multi-sequence file. There is a trade off here between flexibility and
memory usage. In summary:

-  ``Bio.SeqIO.to_dict()`` is the most flexible but also the most memory
   demanding option (see Section [SeqIO:to\_dict]). This is basically a
   helper function to build a normal Python ``dictionary`` with each
   entry held as a ``SeqRecord`` object in memory, allowing you to
   modify the records.

-  ``Bio.SeqIO.index()`` is a useful middle ground, acting like a read
   only dictionary and parsing sequences into ``SeqRecord`` objects on
   demand (see Section [sec:SeqIO-index]).

-  ``Bio.SeqIO.index_db()`` also acts like a read only dictionary but
   stores the identifiers and file offsets in a file on disk (as an
   SQLite3 database), meaning it has very low memory requirements (see
   Section [sec:SeqIO-index-db]), but will be a little bit slower.

See the discussion for an broad overview
(Section [sec:SeqIO-indexing-discussion]).

Sequence files as Dictionaries – In memory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The next thing that we’ll do with our ubiquitous orchid files is to show
how to index them and access them like a database using the Python
``dictionary`` data type (like a hash in Perl). This is very useful for
moderately large files where you only need to access certain elements of
the file, and makes for a nice quick ’n dirty database. For dealing with
larger files where memory becomes a problem, see
Section [sec:SeqIO-index] below.

You can use the function ``Bio.SeqIO.to_dict()`` to make a SeqRecord
dictionary (in memory). By default this will use each record’s
identifier (i.e. the ``.id`` attribute) as the key. Let’s try this using
our GenBank file:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.to_dict(SeqIO.parse("ls_orchid.gbk", "genbank"))

There is just one required argument for ``Bio.SeqIO.to_dict()``, a list
or generator giving ``SeqRecord`` objects. Here we have just used the
output from the ``SeqIO.parse`` function. As the name suggests, this
returns a Python dictionary.

Since this variable ``orchid_dict`` is an ordinary Python dictionary, we
can look at all of the keys we have available:

::

    >>> len(orchid_dict)
    94

::

    >>> list(orchid_dict.keys())
    ['Z78484.1', 'Z78464.1', 'Z78455.1', 'Z78442.1', 'Z78532.1', 'Z78453.1', ..., 'Z78471.1']

You can leave out the “list(...)“ bit if you are still using Python 2.
Under Python 3 the dictionary methods like “.keys()“ and “.values()“ are
iterators rather than lists.

If you really want to, you can even look at all the records at once:

::

    >>> list(orchid_dict.values()) #lots of output!
    ...

We can access a single ``SeqRecord`` object via the keys and manipulate
the object as normal:

::

    >>> seq_record = orchid_dict["Z78475.1"]
    >>> print(seq_record.description)
    P.supardii 5.8S rRNA gene and ITS1 and ITS2 DNA
    >>> print(repr(seq_record.seq))
    Seq('CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGTTGAGATCACAT...GGT', IUPACAmbiguousDNA())

So, it is very easy to create an in memory “database” of our GenBank
records. Next we’ll try this for the FASTA file instead.

Note that those of you with prior Python experience should all be able
to construct a dictionary like this “by hand”. However, typical
dictionary construction methods will not deal with the case of repeated
keys very nicely. Using the ``Bio.SeqIO.to_dict()`` will explicitly
check for duplicate keys, and raise an exception if any are found.

Specifying the dictionary keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the same code as above, but for the FASTA file instead:

::

    from Bio import SeqIO
    orchid_dict = SeqIO.to_dict(SeqIO.parse("ls_orchid.fasta", "fasta"))
    print(orchid_dict.keys())

This time the keys are:

::

    ['gi|2765596|emb|Z78471.1|PDZ78471', 'gi|2765646|emb|Z78521.1|CCZ78521', ...
     ..., 'gi|2765613|emb|Z78488.1|PTZ78488', 'gi|2765583|emb|Z78458.1|PHZ78458']

You should recognise these strings from when we parsed the FASTA file
earlier in Section [sec:fasta-parsing]. Suppose you would rather have
something else as the keys - like the accession numbers. This brings us
nicely to ``SeqIO.to_dict()``\ ’s optional argument ``key_function``,
which lets you define what to use as the dictionary key for your
records.

First you must write your own function to return the key you want (as a
string) when given a ``SeqRecord`` object. In general, the details of
function will depend on the sort of input records you are dealing with.
But for our orchids, we can just split up the record’s identifier using
the “pipe” character (the vertical line) and return the fourth entry
(field three):

::

    def get_accession(record):
        """"Given a SeqRecord, return the accession number as a string.

        e.g. "gi|2765613|emb|Z78488.1|PTZ78488" -> "Z78488.1"
        """
        parts = record.id.split("|")
        assert len(parts) == 5 and parts[0] == "gi" and parts[2] == "emb"
        return parts[3]

Then we can give this function to the ``SeqIO.to_dict()`` function to
use in building the dictionary:

::

    from Bio import SeqIO
    orchid_dict = SeqIO.to_dict(SeqIO.parse("ls_orchid.fasta", "fasta"), key_function=get_accession)
    print(orchid_dict.keys())

Finally, as desired, the new dictionary keys:

::

    >>> print(orchid_dict.keys())
    ['Z78484.1', 'Z78464.1', 'Z78455.1', 'Z78442.1', 'Z78532.1', 'Z78453.1', ..., 'Z78471.1']

Not too complicated, I hope!

Indexing a dictionary using the SEGUID checksum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To give another example of working with dictionaries of ``SeqRecord``
objects, we’ll use the SEGUID checksum function. This is a relatively
recent checksum, and collisions should be very rare (i.e. two different
sequences with the same checksum), an improvement on the CRC64 checksum.

Once again, working with the orchids GenBank file:

::

    from Bio import SeqIO
    from Bio.SeqUtils.CheckSum import seguid
    for record in SeqIO.parse("ls_orchid.gbk", "genbank"):
        print(record.id, seguid(record.seq))

This should give:

::

    Z78533.1 JUEoWn6DPhgZ9nAyowsgtoD9TTo
    Z78532.1 MN/s0q9zDoCVEEc+k/IFwCNF2pY
    ...
    Z78439.1 H+JfaShya/4yyAj7IbMqgNkxdxQ

Now, recall the ``Bio.SeqIO.to_dict()`` function’s ``key_function``
argument expects a function which turns a ``SeqRecord`` into a string.
We can’t use the ``seguid()`` function directly because it expects to be
given a ``Seq`` object (or a string). However, we can use Python’s
``lambda`` feature to create a “one off” function to give to
``Bio.SeqIO.to_dict()`` instead:

::

    >>> from Bio import SeqIO
    >>> from Bio.SeqUtils.CheckSum import seguid
    >>> seguid_dict = SeqIO.to_dict(SeqIO.parse("ls_orchid.gbk", "genbank"),
    ...                             lambda rec : seguid(rec.seq))
    >>> record = seguid_dict["MN/s0q9zDoCVEEc+k/IFwCNF2pY"]
    >>> print(record.id)
    Z78532.1
    >>> print(record.description)
    C.californicum 5.8S rRNA gene and ITS1 and ITS2 DNA

That should have retrieved the record Z78532.1, the second entry in the
file.

Sequence files as Dictionaries – Indexed files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the previous couple of examples tried to illustrate, using
``Bio.SeqIO.to_dict()`` is very flexible. However, because it holds
everything in memory, the size of file you can work with is limited by
your computer’s RAM. In general, this will only work on small to medium
files.

For larger files you should consider ``Bio.SeqIO.index()``, which works
a little differently. Although it still returns a dictionary like
object, this does *not* keep *everything* in memory. Instead, it just
records where each record is within the file – when you ask for a
particular record, it then parses it on demand.

As an example, let’s use the same GenBank file as before:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.index("ls_orchid.gbk", "genbank")
    >>> len(orchid_dict)
    94

::

    >>> orchid_dict.keys()
    ['Z78484.1', 'Z78464.1', 'Z78455.1', 'Z78442.1', 'Z78532.1', 'Z78453.1', ..., 'Z78471.1']

::

    >>> seq_record = orchid_dict["Z78475.1"]
    >>> print(seq_record.description)
    P.supardii 5.8S rRNA gene and ITS1 and ITS2 DNA
    >>> seq_record.seq
    Seq('CGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTGTTGAGATCACAT...GGT', IUPACAmbiguousDNA())
    >>> orchid_dict.close()

Note that ``Bio.SeqIO.index()`` won’t take a handle, but only a
filename. There are good reasons for this, but it is a little technical.
The second argument is the file format (a lower case string as used in
the other ``Bio.SeqIO`` functions). You can use many other simple file
formats, including FASTA and FASTQ files (see the example in
Section [sec:fastq-indexing]). However, alignment formats like PHYLIP or
Clustal are not supported. Finally as an optional argument you can
supply an alphabet, or a key function.

Here is the same example using the FASTA file - all we change is the
filename and the format name:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.index("ls_orchid.fasta", "fasta")
    >>> len(orchid_dict)
    94
    >>> orchid_dict.keys()
    ['gi|2765596|emb|Z78471.1|PDZ78471', 'gi|2765646|emb|Z78521.1|CCZ78521', ...
     ..., 'gi|2765613|emb|Z78488.1|PTZ78488', 'gi|2765583|emb|Z78458.1|PHZ78458']

Specifying the dictionary keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose you want to use the same keys as before? Much like with the
``Bio.SeqIO.to_dict()`` example in
Section [seq:seqio-todict-functionkey], you’ll need to write a tiny
function to map from the FASTA identifier (as a string) to the key you
want:

::

    def get_acc(identifier):
        """"Given a SeqRecord identifier string, return the accession number as a string.

        e.g. "gi|2765613|emb|Z78488.1|PTZ78488" -> "Z78488.1"
        """
        parts = identifier.split("|")
        assert len(parts) == 5 and parts[0] == "gi" and parts[2] == "emb"
        return parts[3]

Then we can give this function to the ``Bio.SeqIO.index()`` function to
use in building the dictionary:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.index("ls_orchid.fasta", "fasta", key_function=get_acc)
    >>> print(orchid_dict.keys())
    ['Z78484.1', 'Z78464.1', 'Z78455.1', 'Z78442.1', 'Z78532.1', 'Z78453.1', ..., 'Z78471.1']

Easy when you know how?

Getting the raw data for a record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The dictionary-like object from ``Bio.SeqIO.index()`` gives you each
entry as a ``SeqRecord`` object. However, it is sometimes useful to be
able to get the original raw data straight from the file. For this use
the ``get_raw()`` method which takes a single argument (the record
identifier) and returns a bytes string (extracted from the file without
modification).

A motivating example is extracting a subset of a records from a large
file where either ``Bio.SeqIO.write()`` does not (yet) support the
output file format (e.g. the plain text SwissProt file format) or where
you need to preserve the text exactly (e.g. GenBank or EMBL output from
Biopython does not yet preserve every last bit of annotation).

Let’s suppose you have download the whole of UniProt in the plain text
SwissPort file format from their FTP site
(ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz)
and uncompressed it as the file ``uniprot_sprot.dat``, and you want to
extract just a few records from it:

::

    >>> from Bio import SeqIO
    >>> uniprot = SeqIO.index("uniprot_sprot.dat", "swiss")
    >>> with open("selected.dat", "wb") as out_handle:
    ...     for acc in ["P33487", "P19801", "P13689", "Q8JZQ5", "Q9TRC7"]:
    ...         out_handle.write(uniprot.get_raw(acc))
    ...

Note with Python 3 onwards, we have to open the file for writing in
binary mode because the ``get_raw()`` method returns bytes strings.

There is a longer example in Section [sec:SeqIO-sort] using the
``SeqIO.index()`` function to sort a large sequence file (without
loading everything into memory at once).

Sequence files as Dictionaries – Database indexed files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Biopython 1.57 introduced an alternative, ``Bio.SeqIO.index_db()``,
which can work on even extremely large files since it stores the record
information as a file on disk (using an SQLite3 database) rather than in
memory. Also, you can index multiple files together (providing all the
record identifiers are unique).

The ``Bio.SeqIO.index()`` function takes three required arguments:

-  Index filename, we suggest using something ending ``.idx``. This
   index file is actually an SQLite3 database.

-  List of sequence filenames to index (or a single filename)

-  File format (lower case string as used in the rest of the ``SeqIO``
   module).

As an example, consider the GenBank flat file releases from the NCBI FTP
site, ftp://ftp.ncbi.nih.gov/genbank/, which are gzip compressed GenBank
files.

As of GenBank release :math:`210`, there are :math:`38` files making up
the viral sequences, ``gbvrl1.seq``, …, ``gbvrl38.seq``, taking about
8GB on disk once decompressed, and containing in total nearly two
million records.

If you were interested in the viruses, you could download all the virus
files from the command line very easily with the ``rsync`` command, and
then decompress them with ``gunzip``:

::

    # For illustration only, see reduced example below
    $ rsync -avP "ftp.ncbi.nih.gov::genbank/gbvrl*.seq.gz" .
    $ gunzip gbvrl*.seq.gz

Unless you care about viruses, that’s a lot of data to download just for
this example - so let’s download *just* the first four chunks (about
25MB each compressed), and decompress them (taking in all about 1GB of
space):

::

    # Reduced example, download only the first four chunks
    $ curl -O ftp://ftp.ncbi.nih.gov/genbank/gbvrl1.seq.gz
    $ curl -O ftp://ftp.ncbi.nih.gov/genbank/gbvrl2.seq.gz
    $ curl -O ftp://ftp.ncbi.nih.gov/genbank/gbvrl3.seq.gz
    $ curl -O ftp://ftp.ncbi.nih.gov/genbank/gbvrl4.seq.gz
    $ gunzip gbvrl*.seq.gz

Now, in Python, index these GenBank files as follows:

::

    >>> import glob
    >>> from Bio import SeqIO
    >>> files = glob.glob("gbvrl*.seq")
    >>> print("%i files to index" % len(files))
    4
    >>> gb_vrl = SeqIO.index_db("gbvrl.idx", files, "genbank")
    >>> print("%i sequences indexed" % len(gb_vrl))
    272960 sequences indexed

Indexing the full set of virus GenBank files took about ten minutes on
my machine, just the first four files took about a minute or so.

However, once done, repeating this will reload the index file
``gbvrl.idx`` in a fraction of a second.

You can use the index as a read only Python dictionary - without having
to worry about which file the sequence comes from, e.g.

::

    >>> print(gb_vrl["AB811634.1"].description)
    Equine encephalosis virus NS3 gene, complete cds, isolate: Kimron1.

Getting the raw data for a record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just as with the ``Bio.SeqIO.index()`` function discussed above in
Section [sec:seqio-index-getraw], the dictionary like object also lets
you get at the raw bytes of each record:

::

    >>> print(gb_vrl.get_raw("AB811634.1"))
    LOCUS       AB811634                 723 bp    RNA     linear   VRL 17-JUN-2015
    DEFINITION  Equine encephalosis virus NS3 gene, complete cds, isolate: Kimron1.
    ACCESSION   AB811634
    ...
    //

Indexing compressed files
~~~~~~~~~~~~~~~~~~~~~~~~~

Very often when you are indexing a sequence file it can be quite large –
so you may want to compress it on disk. Unfortunately efficient random
access is difficult with the more common file formats like gzip and
bzip2. In this setting, BGZF (Blocked GNU Zip Format) can be very
helpful. This is a variant of gzip (and can be decompressed using
standard gzip tools) popularised by the BAM file format,
`samtools <https://www.htslib.org/>`__, and
`tabix <https://www.htslib.org/doc/tabix.html>`__.

To create a BGZF compressed file you can use the command line tool
``bgzip`` which comes with samtools. In our examples we use a filename
extension ``*.bgz``, so they can be distinguished from normal gzipped
files (named ``*.gz``). You can also use the ``Bio.bgzf`` module to read
and write BGZF files from within Python.

The ``Bio.SeqIO.index()`` and ``Bio.SeqIO.index_db()`` can both be used
with BGZF compressed files. For example, if you started with an
uncompressed GenBank file:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.index("ls_orchid.gbk", "genbank")
    >>> len(orchid_dict)
    94
    >>> orchid_dict.close()

You could compress this (while keeping the original file) at the command
line using the following command – but don’t worry, the compressed file
is already included with the other example files:

::

    $ bgzip -c ls_orchid.gbk > ls_orchid.gbk.bgz

You can use the compressed file in exactly the same way:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.index("ls_orchid.gbk.bgz", "genbank")
    >>> len(orchid_dict)
    94
    >>> orchid_dict.close()

or:

::

    >>> from Bio import SeqIO
    >>> orchid_dict = SeqIO.index_db("ls_orchid.gbk.bgz.idx", "ls_orchid.gbk.bgz", "genbank")
    >>> len(orchid_dict)
    94
    >>> orchid_dict.close()

The ``SeqIO`` indexing automatically detects the BGZF compression. Note
that you can’t use the same index file for the uncompressed and
compressed files.

Discussion
~~~~~~~~~~

So, which of these methods should you use and why? It depends on what
you are trying to do (and how much data you are dealing with). However,
in general picking ``Bio.SeqIO.index()`` is a good starting point. If
you are dealing with millions of records, multiple files, or repeated
analyses, then look at ``Bio.SeqIO.index_db()``.

Reasons to choose ``Bio.SeqIO.to_dict()`` over either
``Bio.SeqIO.index()`` or ``Bio.SeqIO.index_db()`` boil down to a need
for flexibility despite its high memory needs. The advantage of storing
the ``SeqRecord`` objects in memory is they can be changed, added to, or
removed at will. In addition to the downside of high memory consumption,
indexing can also take longer because all the records must be fully
parsed.

Both ``Bio.SeqIO.index()`` and ``Bio.SeqIO.index_db()`` only parse
records on demand. When indexing, they scan the file once looking for
the start of each record and do as little work as possible to extract
the identifier.

Reasons to choose ``Bio.SeqIO.index()`` over ``Bio.SeqIO.index_db()``
include:

-  Faster to build the index (more noticeable in simple file formats)

-  Slightly faster access as SeqRecord objects (but the difference is
   only really noticeable for simple to parse file formats).

-  Can use any immutable Python object as the dictionary keys (e.g. a
   tuple of strings, or a frozen set) not just strings.

-  Don’t need to worry about the index database being out of date if the
   sequence file being indexed has changed.

Reasons to choose ``Bio.SeqIO.index_db()`` over ``Bio.SeqIO.index()``
include:

-  Not memory limited – this is already important with files from second
   generation sequencing where 10s of millions of sequences are common,
   and using ``Bio.SeqIO.index()`` can require more than 4GB of RAM and
   therefore a 64bit version of Python.

-  Because the index is kept on disk, it can be reused. Although
   building the index database file takes longer, if you have a script
   which will be rerun on the same datafiles in future, this could save
   time in the long run.

-  Indexing multiple files together

-  The ``get_raw()`` method can be much faster, since for most file
   formats the length of each record is stored as well as its offset.

Writing Sequence Files
----------------------

We’ve talked about using ``Bio.SeqIO.parse()`` for sequence input
(reading files), and now we’ll look at ``Bio.SeqIO.write()`` which is
for sequence output (writing files). This is a function taking three
arguments: some ``SeqRecord`` objects, a handle or filename to write to,
and a sequence format.

Here is an example, where we start by creating a few ``SeqRecord``
objects the hard way (by hand, rather than by loading them from a file):

::

    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Alphabet import generic_protein

    rec1 = SeqRecord(Seq("MMYQQGCFAGGTVLRLAKDLAENNRGARVLVVCSEITAVTFRGPSETHLDSMVGQALFGD" \
                        +"GAGAVIVGSDPDLSVERPLYELVWTGATLLPDSEGAIDGHLREVGLTFHLLKDVPGLISK" \
                        +"NIEKSLKEAFTPLGISDWNSTFWIAHPGGPAILDQVEAKLGLKEEKMRATREVLSEYGNM" \
                        +"SSAC", generic_protein),
                     id="gi|14150838|gb|AAK54648.1|AF376133_1",
                     description="chalcone synthase [Cucumis sativus]")

    rec2 = SeqRecord(Seq("YPDYYFRITNREHKAELKEKFQRMCDKSMIKKRYMYLTEEILKENPSMCEYMAPSLDARQ" \
                        +"DMVVVEIPKLGKEAAVKAIKEWGQ", generic_protein),
                     id="gi|13919613|gb|AAK33142.1|",
                     description="chalcone synthase [Fragaria vesca subsp. bracteata]")

    rec3 = SeqRecord(Seq("MVTVEEFRRAQCAEGPATVMAIGTATPSNCVDQSTYPDYYFRITNSEHKVELKEKFKRMC" \
                        +"EKSMIKKRYMHLTEEILKENPNICAYMAPSLDARQDIVVVEVPKLGKEAAQKAIKEWGQP" \
                        +"KSKITHLVFCTTSGVDMPGCDYQLTKLLGLRPSVKRFMMYQQGCFAGGTVLRMAKDLAEN" \
                        +"NKGARVLVVCSEITAVTFRGPNDTHLDSLVGQALFGDGAAAVIIGSDPIPEVERPLFELV" \
                        +"SAAQTLLPDSEGAIDGHLREVGLTFHLLKDVPGLISKNIEKSLVEAFQPLGISDWNSLFW" \
                        +"IAHPGGPAILDQVELKLGLKQEKLKATRKVLSNYGNMSSACVLFILDEMRKASAKEGLGT" \
                        +"TGEGLEWGVLFGFGPGLTVETVVLHSVAT", generic_protein),
                     id="gi|13925890|gb|AAK49457.1|",
                     description="chalcone synthase [Nicotiana tabacum]")

    my_records = [rec1, rec2, rec3]

Now we have a list of ``SeqRecord`` objects, we’ll write them to a FASTA
format file:

::

    from Bio import SeqIO
    SeqIO.write(my_records, "my_example.faa", "fasta")

And if you open this file in your favourite text editor it should look
like this:

::

    >gi|14150838|gb|AAK54648.1|AF376133_1 chalcone synthase [Cucumis sativus]
    MMYQQGCFAGGTVLRLAKDLAENNRGARVLVVCSEITAVTFRGPSETHLDSMVGQALFGD
    GAGAVIVGSDPDLSVERPLYELVWTGATLLPDSEGAIDGHLREVGLTFHLLKDVPGLISK
    NIEKSLKEAFTPLGISDWNSTFWIAHPGGPAILDQVEAKLGLKEEKMRATREVLSEYGNM
    SSAC
    >gi|13919613|gb|AAK33142.1| chalcone synthase [Fragaria vesca subsp. bracteata]
    YPDYYFRITNREHKAELKEKFQRMCDKSMIKKRYMYLTEEILKENPSMCEYMAPSLDARQ
    DMVVVEIPKLGKEAAVKAIKEWGQ
    >gi|13925890|gb|AAK49457.1| chalcone synthase [Nicotiana tabacum]
    MVTVEEFRRAQCAEGPATVMAIGTATPSNCVDQSTYPDYYFRITNSEHKVELKEKFKRMC
    EKSMIKKRYMHLTEEILKENPNICAYMAPSLDARQDIVVVEVPKLGKEAAQKAIKEWGQP
    KSKITHLVFCTTSGVDMPGCDYQLTKLLGLRPSVKRFMMYQQGCFAGGTVLRMAKDLAEN
    NKGARVLVVCSEITAVTFRGPNDTHLDSLVGQALFGDGAAAVIIGSDPIPEVERPLFELV
    SAAQTLLPDSEGAIDGHLREVGLTFHLLKDVPGLISKNIEKSLVEAFQPLGISDWNSLFW
    IAHPGGPAILDQVELKLGLKQEKLKATRKVLSNYGNMSSACVLFILDEMRKASAKEGLGT
    TGEGLEWGVLFGFGPGLTVETVVLHSVAT

Suppose you wanted to know how many records the ``Bio.SeqIO.write()``
function wrote to the handle? If your records were in a list you could
just use ``len(my_records)``, however you can’t do that when your
records come from a generator/iterator. The ``Bio.SeqIO.write()``
function returns the number of ``SeqRecord`` objects written to the
file.

*Note* - If you tell the ``Bio.SeqIO.write()`` function to write to a
file that already exists, the old file will be overwritten without any
warning.

Round trips
~~~~~~~~~~~

Some people like their parsers to be “round-tripable”, meaning if you
read in a file and write it back out again it is unchanged. This
requires that the parser must extract enough information to reproduce
the original file *exactly*. ``Bio.SeqIO`` does *not* aim to do this.

As a trivial example, any line wrapping of the sequence data in FASTA
files is allowed. An identical ``SeqRecord`` would be given from parsing
the following two examples which differ only in their line breaks:

::

    >YAL068C-7235.2170 Putative promoter sequence
    TACGAGAATAATTTCTCATCATCCAGCTTTAACACAAAATTCGCACAGTTTTCGTTAAGA
    GAACTTAACATTTTCTTATGACGTAAATGAAGTTTATATATAAATTTCCTTTTTATTGGA

    >YAL068C-7235.2170 Putative promoter sequence
    TACGAGAATAATTTCTCATCATCCAGCTTTAACACAAAATTCGCA
    CAGTTTTCGTTAAGAGAACTTAACATTTTCTTATGACGTAAATGA
    AGTTTATATATAAATTTCCTTTTTATTGGA

To make a round-tripable FASTA parser you would need to keep track of
where the sequence line breaks occurred, and this extra information is
usually pointless. Instead Biopython uses a default line wrapping of
:math:`60` characters on output. The same problem with white space
applies in many other file formats too. Another issue in some cases is
that Biopython does not (yet) preserve every last bit of annotation
(e.g. GenBank and EMBL).

Occasionally preserving the original layout (with any quirks it may
have) is important. See Section [sec:seqio-index-getraw] about the
``get_raw()`` method of the ``Bio.SeqIO.index()`` dictionary-like object
for one potential solution.

Converting between sequence file formats
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In previous example we used a list of ``SeqRecord`` objects as input to
the ``Bio.SeqIO.write()`` function, but it will also accept a
``SeqRecord`` iterator like we get from ``Bio.SeqIO.parse()`` – this
lets us do file conversion by combining these two functions.

For this example we’ll read in the GenBank format file
`ls\_orchid.gbk <https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.gbk>`__
and write it out in FASTA format:

::

    from Bio import SeqIO
    records = SeqIO.parse("ls_orchid.gbk", "genbank")
    count = SeqIO.write(records, "my_example.fasta", "fasta")
    print("Converted %i records" % count)

Still, that is a little bit complicated. So, because file conversion is
such a common task, there is a helper function letting you replace that
with just:

::

    from Bio import SeqIO
    count = SeqIO.convert("ls_orchid.gbk", "genbank", "my_example.fasta", "fasta")
    print("Converted %i records" % count)

The ``Bio.SeqIO.convert()`` function will take handles *or* filenames.
Watch out though – if the output file already exists, it will overwrite
it! To find out more, see the built in help:

::

    >>> from Bio import SeqIO
    >>> help(SeqIO.convert)
    ...

In principle, just by changing the filenames and the format names, this
code could be used to convert between any file formats available in
Biopython. However, writing some formats requires information (e.g.
quality scores) which other files formats don’t contain. For example,
while you can turn a FASTQ file into a FASTA file, you can’t do the
reverse. See also Sections [sec:SeqIO-fastq-conversion]
and [sec:SeqIO-fasta-qual-conversion] in the cookbook chapter which
looks at inter-converting between different FASTQ formats.

Finally, as an added incentive for using the ``Bio.SeqIO.convert()``
function (on top of the fact your code will be shorter), doing it this
way may also be faster! The reason for this is the convert function can
take advantage of several file format specific optimisations and tricks.

Converting a file of sequences to their reverse complements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you had a file of nucleotide sequences, and you wanted to turn
it into a file containing their reverse complement sequences. This time
a little bit of work is required to transform the ``SeqRecord`` objects
we get from our input file into something suitable for saving to our
output file.

To start with, we’ll use ``Bio.SeqIO.parse()`` to load some nucleotide
sequences from a file, then print out their reverse complements using
the ``Seq`` object’s built in ``.reverse_complement()`` method (see
Section [sec:seq-reverse-complement]):

::

    >>> from Bio import SeqIO
    >>> for record in SeqIO.parse("ls_orchid.gbk", "genbank"):
    ...     print(record.id)
    ...     print(record.seq.reverse_complement())

Now, if we want to save these reverse complements to a file, we’ll need
to make ``SeqRecord`` objects. We can use the ``SeqRecord`` object’s
built in ``.reverse_complement()`` method (see
Section [sec:SeqRecord-reverse-complement]) but we must decide how to
name our new records.

This is an excellent place to demonstrate the power of list
comprehensions which make a list in memory:

::

    >>> from Bio import SeqIO
    >>> records = [rec.reverse_complement(id="rc_"+rec.id, description = "reverse complement") \
    ...            for rec in SeqIO.parse("ls_orchid.fasta", "fasta")]
    >>> len(records)
    94

Now list comprehensions have a nice trick up their sleeves, you can add
a conditional statement:

::

    >>> records = [rec.reverse_complement(id="rc_"+rec.id, description = "reverse complement") \
    ...            for rec in SeqIO.parse("ls_orchid.fasta", "fasta") if len(rec)<700]
    >>> len(records)
    18

That would create an in memory list of reverse complement records where
the sequence length was under 700 base pairs. However, we can do exactly
the same with a generator expression - but with the advantage that this
does not create a list of all the records in memory at once:

::

    >>> records = (rec.reverse_complement(id="rc_"+rec.id, description = "reverse complement") \
    ...           for rec in SeqIO.parse("ls_orchid.fasta", "fasta") if len(rec)<700)

As a complete example:

::

    >>> from Bio import SeqIO
    >>> records = (rec.reverse_complement(id="rc_"+rec.id, description = "reverse complement") \
    ...            for rec in SeqIO.parse("ls_orchid.fasta", "fasta") if len(rec)<700)
    >>> SeqIO.write(records, "rev_comp.fasta", "fasta")
    18

There is a related example in Section [sec:SeqIO-translate], translating
each record in a FASTA file from nucleotides to amino acids.

Getting your SeqRecord objects as formatted strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose that you don’t really want to write your records to a file or
handle – instead you want a string containing the records in a
particular file format. The ``Bio.SeqIO`` interface is based on handles,
but Python has a useful built in module which provides a string based
handle.

For an example of how you might use this, let’s load in a bunch of
``SeqRecord`` objects from our orchids GenBank file, and create a string
containing the records in FASTA format:

::

    from Bio import SeqIO
    from StringIO import StringIO
    records = SeqIO.parse("ls_orchid.gbk", "genbank")
    out_handle = StringIO()
    SeqIO.write(records, out_handle, "fasta")
    fasta_data = out_handle.getvalue()
    print(fasta_data)

This isn’t entirely straightforward the first time you see it! On the
bright side, for the special case where you would like a string
containing a *single* record in a particular file format, use the the
``SeqRecord`` class’ ``format()`` method (see
Section [sec:SeqRecord-format]).

Note that although we don’t encourage it, you *can* use the ``format()``
method to write to a file, for example something like this:

::

    from Bio import SeqIO
    with open("ls_orchid_long.tab", "w") as out_handle:
        for record in SeqIO.parse("ls_orchid.gbk", "genbank"):
            if len(record) > 100:
                out_handle.write(record.format("tab"))

While this style of code will work for a simple sequential file format
like FASTA or the simple tab separated format used here, it will *not*
work for more complex or interlaced file formats. This is why we still
recommend using ``Bio.SeqIO.write()``, as in the following example:

::

    from Bio import SeqIO
    records = (rec for rec in SeqIO.parse("ls_orchid.gbk", "genbank") if len(rec) > 100)
    SeqIO.write(records, "ls_orchid.tab", "tab")

Making a single call to ``SeqIO.write(...)`` is also much quicker than
multiple calls to the ``SeqRecord.format(...)`` method.

Low level FASTA and FASTQ parsers
---------------------------------

Working with the low-level ``SimpleFastaParser`` or
``FastqGeneralIterator`` is often more practical than
``Bio.SeqIO.parse`` when dealing with large high-throughput FASTA or
FASTQ sequencing files where speed matters. As noted in the introduction
to this chapter, the file-format neutral ``Bio.SeqIO`` interface has the
overhead of creating many objects even for simple formats like FASTA.

When parsing FASTA files, internally ``Bio.SeqIO.parse()`` calls the
low-level ``SimpleFastaParser`` with the file handle. You can use this
directly - it iterates over the file handle returning each record as a
tuple of two strings, the title line (everything after the ``>``
character) and the sequence (as a plain string):

::

    >>> from Bio.SeqIO.FastaIO import SimpleFastaParser
    >>> count = 0
    >>> total_len = 0
    >>> with open("ls_orchid.fasta") as in_handle:
    ...     for title, seq in SimpleFastaParser(in_handle):
    ...         count += 1
    ...         total_len += len(seq)
    ...
    >>> print("%i records with total sequence length %i" % (count, total_len))
    94 records with total sequence length 67518

As long as you don’t care about line wrapping (and you probably don’t
for short read high-througput data), then outputing FASTA format from
these strings is also very fast:

::

    ...
    out_handle.write(">%s\n%s\n" % (title, seq))
    ...

Likewise, when parsing FASTQ files, internally ``Bio.SeqIO.parse()``
calls the low-level ``FastqGeneralIterator`` with the file handle. If
you don’t need the quality scores turned into integers, or can work with
them as ASCII strings this is ideal:

::

    >>> from Bio.SeqIO.QualityIO import FastqGeneralIterator
    >>> count = 0
    >>> total_len = 0
    >>> with open("example.fastq") as in_handle:
    ...     for title, seq, qual in FastqGeneralIterator(in_handle):
    ...         count += 1
    ...         total_len += len(seq)
    ...
    >>> print("%i records with total sequence length %i" % (count, total_len))
    3 records with total sequence length 75

There are more examples of this in the Cookbook
(Chapter [chapter:cookbook]), including how to output FASTQ efficiently
from strings using this code snippet:

::

    ...
    out_handle.write("@%s\n%s\n+\n%s\n" % (title, seq, qual))
    ...
