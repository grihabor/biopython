.. chapter:SeqRecord:

Sequence annotation objects
===========================

Chapter \ `[chapter:Bio.Seq] <#chapter:Bio.Seq>`__ introduced the
sequence classes. Immediately “above” the ``Seq`` class is the Sequence
Record or ``SeqRecord`` class, defined in the ``Bio.SeqRecord`` module.
This class allows higher level features such as identifiers and features
(as ``SeqFeature`` objects) to be associated with the sequence, and is
used throughout the sequence input/output interface ``Bio.SeqIO``
described fully in
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__.

If you are only going to be working with simple data like FASTA files,
you can probably skip this chapter for now. If on the other hand you are
going to be using richly annotated sequence data, say from GenBank or
EMBL files, this information is quite important.

While this chapter should cover most things to do with the ``SeqRecord``
and ``SeqFeature`` objects in this chapter, you may also want to read
the ``SeqRecord`` wiki page (http://biopython.org/wiki/SeqRecord), and
the built in documentation (also online –
`SeqRecord <http://biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html>`__
and
`SeqFeature <http://biopython.org/DIST/docs/api/Bio.SeqFeature.SeqFeature-class.html>`__):

::

    >>> from Bio.SeqRecord import SeqRecord
    >>> help(SeqRecord)
    ...

.. sec:SeqRecord:

The SeqRecord object
--------------------

The ``SeqRecord`` (Sequence Record) class is defined in the
``Bio.SeqRecord`` module. This class allows higher level features such
as identifiers and features to be associated with a sequence (see
Chapter \ `[chapter:Bio.Seq] <#chapter:Bio.Seq>`__), and is the basic
data type for the ``Bio.SeqIO`` sequence input/output interface (see
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__).

The ``SeqRecord`` class itself is quite simple, and offers the following
information as attributes:

.seq
    – The sequence itself, typically a ``Seq`` object.

.id
    – The primary ID used to identify the sequence – a string. In most
    cases this is something like an accession number.

.name
    – A “common” name/id for the sequence – a string. In some cases this
    will be the same as the accession number, but it could also be a
    clone name. I think of this as being analogous to the LOCUS id in a
    GenBank record.

.description
    – A human readable description or expressive name for the sequence –
    a string.

.letter_annotations
    – Holds per-letter-annotations using a (restricted) dictionary of
    additional information about the letters in the sequence. The keys
    are the name of the information, and the information is contained in
    the value as a Python sequence (i.e. a list, tuple or string) with
    the same length as the sequence itself. This is often used for
    quality scores (e.g.
    Section \ `[sec:FASTQ-filtering-example] <#sec:FASTQ-filtering-example>`__)
    or secondary structure information (e.g. from Stockholm/PFAM
    alignment files).

.annotations
    – A dictionary of additional information about the sequence. The
    keys are the name of the information, and the information is
    contained in the value. This allows the addition of more
    “unstructured” information to the sequence.

.features
    – A list of ``SeqFeature`` objects with more structured information
    about the features on a sequence (e.g. position of genes on a
    genome, or domains on a protein sequence). The structure of sequence
    features is described below in Section \ `3 <#sec:seq_features>`__.

.dbxrefs
    - A list of database cross-references as strings.

Creating a SeqRecord
--------------------

Using a ``SeqRecord`` object is not very complicated, since all of the
information is presented as attributes of the class. Usually you won’t
create a ``SeqRecord`` “by hand”, but instead use ``Bio.SeqIO`` to read
in a sequence file for you (see
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__ and the examples
below). However, creating ``SeqRecord`` can be quite simple.

SeqRecord objects from scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a ``SeqRecord`` at a minimum you just need a ``Seq`` object:

::

    >>> from Bio.Seq import Seq
    >>> simple_seq = Seq("GATC")
    >>> from Bio.SeqRecord import SeqRecord
    >>> simple_seq_r = SeqRecord(simple_seq)

Additionally, you can also pass the id, name and description to the
initialization function, but if not they will be set as strings
indicating they are unknown, and can be modified subsequently:

::

    >>> simple_seq_r.id
    '<unknown id>'
    >>> simple_seq_r.id = "AC12345"
    >>> simple_seq_r.description = "Made up sequence I wish I could write a paper about"
    >>> print(simple_seq_r.description)
    Made up sequence I wish I could write a paper about
    >>> simple_seq_r.seq
    Seq('GATC', Alphabet())

Including an identifier is very important if you want to output your
``SeqRecord`` to a file. You would normally include this when creating
the object:

::

    >>> from Bio.Seq import Seq
    >>> simple_seq = Seq("GATC")
    >>> from Bio.SeqRecord import SeqRecord
    >>> simple_seq_r = SeqRecord(simple_seq, id="AC12345")

As mentioned above, the ``SeqRecord`` has an dictionary attribute
``annotations``. This is used for any miscellaneous annotations that
doesn’t fit under one of the other more specific attributes. Adding
annotations is easy, and just involves dealing directly with the
annotation dictionary:

::

    >>> simple_seq_r.annotations["evidence"] = "None. I just made it up."
    >>> print(simple_seq_r.annotations)
    {'evidence': 'None. I just made it up.'}
    >>> print(simple_seq_r.annotations["evidence"])
    None. I just made it up.

Working with per-letter-annotations is similar, ``letter_annotations``
is a dictionary like attribute which will let you assign any Python
sequence (i.e. a string, list or tuple) which has the same length as the
sequence:

::

    >>> simple_seq_r.letter_annotations["phred_quality"] = [40, 40, 38, 30]
    >>> print(simple_seq_r.letter_annotations)
    {'phred_quality': [40, 40, 38, 30]}
    >>> print(simple_seq_r.letter_annotations["phred_quality"])
    [40, 40, 38, 30]

The ``dbxrefs`` and ``features`` attributes are just Python lists, and
should be used to store strings and ``SeqFeature`` objects (discussed
later in this chapter) respectively.

SeqRecord objects from FASTA files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example uses a fairly large FASTA file containing the whole
sequence for *Yersinia pestis biovar Microtus* str. 91001 plasmid pPCP1,
originally downloaded from the NCBI. This file is included with the
Biopython unit tests under the GenBank folder, or online
```NC_005816.fna`` <https://raw.githubusercontent.com/biopython/biopython/master/Tests/GenBank/NC_005816.fna>`__
from our website.

The file starts like this - and you can check there is only one record
present (i.e. only one line starting with a greater than symbol):

::

    >gi|45478711|ref|NC_005816.1| Yersinia pestis biovar Microtus ... pPCP1, complete sequence
    TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGGGGGTAATCTGCTCTCC
    ...

Back in Chapter \ `[chapter:quick-start] <#chapter:quick-start>`__ you
will have seen the function ``Bio.SeqIO.parse(...)`` used to loop over
all the records in a file as ``SeqRecord`` objects. The ``Bio.SeqIO``
module has a sister function for use on files which contain just one
record which we’ll use here (see
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__ for details):

::

    >>> from Bio import SeqIO
    >>> record = SeqIO.read("NC_005816.fna", "fasta")
    >>> record
    SeqRecord(seq=Seq('TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGG...CTG',
    SingleLetterAlphabet()), id='gi|45478711|ref|NC_005816.1|', name='gi|45478711|ref|NC_005816.1|',
    description='gi|45478711|ref|NC_005816.1| Yersinia pestis biovar Microtus ... sequence',
    dbxrefs=[])

Now, let’s have a look at the key attributes of this ``SeqRecord``
individually – starting with the ``seq`` attribute which gives you a
``Seq`` object:

::

    >>> record.seq
    Seq('TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGG...CTG', SingleLetterAlphabet())

Here ``Bio.SeqIO`` has defaulted to a generic alphabet, rather than
guessing that this is DNA. If you know in advance what kind of sequence
your FASTA file contains, you can tell ``Bio.SeqIO`` which alphabet to
use (see Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__).

Next, the identifiers and description:

::

    >>> record.id
    'gi|45478711|ref|NC_005816.1|'
    >>> record.name
    'gi|45478711|ref|NC_005816.1|'
    >>> record.description
    'gi|45478711|ref|NC_005816.1| Yersinia pestis biovar Microtus ... pPCP1, complete sequence'

As you can see above, the first word of the FASTA record’s title line
(after removing the greater than symbol) is used for both the ``id`` and
``name`` attributes. The whole title line (after removing the greater
than symbol) is used for the record description. This is deliberate,
partly for backwards compatibility reasons, but it also makes sense if
you have a FASTA file like this:

::

    >Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1
    TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGGGGGTAATCTGCTCTCC
    ...

Note that none of the other annotation attributes get populated when
reading a FASTA file:

::

    >>> record.dbxrefs
    []
    >>> record.annotations
    {}
    >>> record.letter_annotations
    {}
    >>> record.features
    []

In this case our example FASTA file was from the NCBI, and they have a
fairly well defined set of conventions for formatting their FASTA lines.
This means it would be possible to parse this information and extract
the GI number and accession for example. However, FASTA files from other
sources vary, so this isn’t possible in general.

SeqRecord objects from GenBank files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As in the previous example, we’re going to look at the whole sequence
for *Yersinia pestis biovar Microtus* str. 91001 plasmid pPCP1,
originally downloaded from the NCBI, but this time as a GenBank file.
Again, this file is included with the Biopython unit tests under the
GenBank folder, or online
```NC_005816.gb`` <https://raw.githubusercontent.com/biopython/biopython/master/Tests/GenBank/NC_005816.gb>`__
from our website.

This file contains a single record (i.e. only one LOCUS line) and
starts:

::

    LOCUS       NC_005816               9609 bp    DNA     circular BCT 21-JUL-2008
    DEFINITION  Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete
                sequence.
    ACCESSION   NC_005816
    VERSION     NC_005816.1  GI:45478711
    PROJECT     GenomeProject:10638
    ...

Again, we’ll use ``Bio.SeqIO`` to read this file in, and the code is
almost identical to that for used above for the FASTA file (see
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__ for details):

::

    >>> from Bio import SeqIO
    >>> record = SeqIO.read("NC_005816.gb", "genbank")
    >>> record
    SeqRecord(seq=Seq('TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGG...CTG',
    IUPACAmbiguousDNA()), id='NC_005816.1', name='NC_005816',
    description='Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence.',
    dbxrefs=['Project:10638'])

You should be able to spot some differences already! But taking the
attributes individually, the sequence string is the same as before, but
this time ``Bio.SeqIO`` has been able to automatically assign a more
specific alphabet (see
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__ for details):

::

    >>> record.seq
    Seq('TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGG...CTG', IUPACAmbiguousDNA())

The ``name`` comes from the LOCUS line, while the ``id`` includes the
version suffix. The description comes from the DEFINITION line:

::

    >>> record.id
    'NC_005816.1'
    >>> record.name
    'NC_005816'
    >>> record.description
    'Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence.'

GenBank files don’t have any per-letter annotations:

::

    >>> record.letter_annotations
    {}

Most of the annotations information gets recorded in the ``annotations``
dictionary, for example:

::

    >>> len(record.annotations)
    11
    >>> record.annotations["source"]
    'Yersinia pestis biovar Microtus str. 91001'

The ``dbxrefs`` list gets populated from any PROJECT or DBLINK lines:

::

    >>> record.dbxrefs
    ['Project:10638']

Finally, and perhaps most interestingly, all the entries in the features
table (e.g. the genes or CDS features) get recorded as ``SeqFeature``
objects in the ``features`` list.

::

    >>> len(record.features)
    29

We’ll talk about ``SeqFeature`` objects next, in
Section \ `3 <#sec:seq_features>`__.

.. sec:seq_features:

Feature, location and position objects
--------------------------------------

SeqFeature objects
~~~~~~~~~~~~~~~~~~

Sequence features are an essential part of describing a sequence. Once
you get beyond the sequence itself, you need some way to organize and
easily get at the more “abstract” information that is known about the
sequence. While it is probably impossible to develop a general sequence
feature class that will cover everything, the Biopython ``SeqFeature``
class attempts to encapsulate as much of the information about the
sequence as possible. The design is heavily based on the GenBank/EMBL
feature tables, so if you understand how they look, you’ll probably have
an easier time grasping the structure of the Biopython classes.

The key idea about each ``SeqFeature`` object is to describe a region on
a parent sequence, typically a ``SeqRecord`` object. That region is
described with a location object, typically a range between two
positions (see Section \ `3.2 <#sec:locations>`__ below).

The ``SeqFeature`` class has a number of attributes, so first we’ll list
them and their general features, and then later in the chapter work
through examples to show how this applies to a real life example. The
attributes of a SeqFeature are:

.type
    – This is a textual description of the type of feature (for
    instance, this will be something like ‘CDS’ or ‘gene’).

.location
    – The location of the ``SeqFeature`` on the sequence that you are
    dealing with, see Section \ `3.2 <#sec:locations>`__ below. The
    ``SeqFeature`` delegates much of its functionality to the location
    object, and includes a number of shortcut attributes for properties
    of the location:

    .ref
        – shorthand for ``.location.ref`` – any (different) reference
        sequence the location is referring to. Usually just None.

    .ref_db
        – shorthand for ``.location.ref_db`` – specifies the database
        any identifier in ``.ref`` refers to. Usually just None.

    .strand
        – shorthand for ``.location.strand`` – the strand on the
        sequence that the feature is located on. For double stranded
        nucleotide sequence this may either be :math:`1` for the top
        strand, :math:`-1` for the bottom strand, :math:`0` if the
        strand is important but is unknown, or ``None`` if it doesn’t
        matter. This is None for proteins, or single stranded sequences.

.qualifiers
    – This is a Python dictionary of additional information about the
    feature. The key is some kind of terse one-word description of what
    the information contained in the value is about, and the value is
    the actual information. For example, a common key for a qualifier
    might be “evidence” and the value might be “computational
    (non-experimental).” This is just a way to let the person who is
    looking at the feature know that it has not be experimentally
    (i. e. in a wet lab) confirmed. Note that other the value will be a
    list of strings (even when there is only one string). This is a
    reflection of the feature tables in GenBank/EMBL files.

.sub_features
    – This used to be used to represent features with complicated
    locations like ‘joins’ in GenBank/EMBL files. This has been
    deprecated with the introduction of the ``CompoundLocation`` object,
    and should now be ignored.

.. sec:locations:

Positions and locations
~~~~~~~~~~~~~~~~~~~~~~~

The key idea about each ``SeqFeature`` object is to describe a region on
a parent sequence, for which we use a location object, typically
describing a range between two positions. Two try to clarify the
terminology we’re using:

position
    – This refers to a single position on a sequence, which may be fuzzy
    or not. For instance, 5, 20, ``<100`` and ``>200`` are all
    positions.

location
    – A location is region of sequence bounded by some positions. For
    instance 5..20 (i. e. 5 to 20) is a location.

I just mention this because sometimes I get confused between the two.

FeatureLocation object
^^^^^^^^^^^^^^^^^^^^^^

Unless you work with eukaryotic genes, most ``SeqFeature`` locations are
extremely simple - you just need start and end coordinates and a strand.
That’s essentially all the basic ``FeatureLocation`` object does.

In practise of course, things can be more complicated. First of all we
have to handle compound locations made up of several regions. Secondly,
the positions themselves may be fuzzy (inexact).

CompoundLocation object
^^^^^^^^^^^^^^^^^^^^^^^

Biopython 1.62 introduced the ``CompoundLocation`` as part of a
restructuring of how complex locations made up of multiple regions are
represented. The main usage is for handling ‘join’ locations in
EMBL/GenBank files.

Fuzzy Positions
^^^^^^^^^^^^^^^

So far we’ve only used simple positions. One complication in dealing
with feature locations comes in the positions themselves. In biology
many times things aren’t entirely certain (as much as us wet lab
biologists try to make them certain!). For instance, you might do a
dinucleotide priming experiment and discover that the start of mRNA
transcript starts at one of two sites. This is very useful information,
but the complication comes in how to represent this as a position. To
help us deal with this, we have the concept of fuzzy positions.
Basically there are several types of fuzzy positions, so we have five
classes do deal with them:

ExactPosition
    – As its name suggests, this class represents a position which is
    specified as exact along the sequence. This is represented as just a
    number, and you can get the position by looking at the ``position``
    attribute of the object.

BeforePosition
    – This class represents a fuzzy position that occurs prior to some
    specified site. In GenBank/EMBL notation, this is represented as
    something like :literal:`\`<13'`, signifying that the real position
    is located somewhere less than 13. To get the specified upper
    boundary, look at the ``position`` attribute of the object.

AfterPosition
    – Contrary to ``BeforePosition``, this class represents a position
    that occurs after some specified site. This is represented in
    GenBank as :literal:`\`>13'`, and like ``BeforePosition``, you get
    the boundary number by looking at the ``position`` attribute of the
    object.

WithinPosition
    – Occasionally used for GenBank/EMBL locations, this class models a
    position which occurs somewhere between two specified nucleotides.
    In GenBank/EMBL notation, this would be represented as ‘(1.5)’, to
    represent that the position is somewhere within the range 1 to 5. To
    get the information in this class you have to look at two
    attributes. The ``position`` attribute specifies the lower boundary
    of the range we are looking at, so in our example case this would be
    one. The ``extension`` attribute specifies the range to the higher
    boundary, so in this case it would be 4. So ``object.position`` is
    the lower boundary and ``object.position + object.extension`` is the
    upper boundary.

OneOfPosition
    – Occasionally used for GenBank/EMBL locations, this class deals
    with a position where several possible values exist, for instance
    you could use this if the start codon was unclear and there where
    two candidates for the start of the gene. Alternatively, that might
    be handled explicitly as two related gene features.

UnknownPosition
    – This class deals with a position of unknown location. This is not
    used in GenBank/EMBL, but corresponds to the ‘?’ feature coordinate
    used in UniProt.

Here’s an example where we create a location with fuzzy end points:

::

    >>> from Bio import SeqFeature
    >>> start_pos = SeqFeature.AfterPosition(5)
    >>> end_pos = SeqFeature.BetweenPosition(9, left=8, right=9)
    >>> my_location = SeqFeature.FeatureLocation(start_pos, end_pos)

Note that the details of some of the fuzzy-locations changed in
Biopython 1.59, in particular for BetweenPosition and WithinPosition you
must now make it explicit which integer position should be used for
slicing etc. For a start position this is generally the lower (left)
value, while for an end position this would generally be the higher
(right) value.

If you print out a ``FeatureLocation`` object, you can get a nice
representation of the information:

::

    >>> print(my_location)
    [>5:(8^9)]

We can access the fuzzy start and end positions using the start and end
attributes of the location:

::

    >>> my_location.start
    AfterPosition(5)
    >>> print(my_location.start)
    >5
    >>> my_location.end
    BetweenPosition(9, left=8, right=9)
    >>> print(my_location.end)
    (8^9)

If you don’t want to deal with fuzzy positions and just want numbers,
they are actually subclasses of integers so should work like integers:

::

    >>> int(my_location.start)
    5
    >>> int(my_location.end)
    9

For compatibility with older versions of Biopython you can ask for the
``nofuzzy_start`` and ``nofuzzy_end`` attributes of the location which
are plain integers:

::

    >>> my_location.nofuzzy_start
    5
    >>> my_location.nofuzzy_end
    9

Notice that this just gives you back the position attributes of the
fuzzy locations.

Similarly, to make it easy to create a position without worrying about
fuzzy positions, you can just pass in numbers to the ``FeaturePosition``
constructors, and you’ll get back out ``ExactPosition`` objects:

::

    >>> exact_location = SeqFeature.FeatureLocation(5, 9)
    >>> print(exact_location)
    [5:9]
    >>> exact_location.start
    ExactPosition(5)
    >>> int(exact_location.start)
    5
    >>> exact_location.nofuzzy_start
    5

That is most of the nitty gritty about dealing with fuzzy positions in
Biopython. It has been designed so that dealing with fuzziness is not
that much more complicated than dealing with exact positions, and
hopefully you find that true!

Location testing
^^^^^^^^^^^^^^^^

You can use the Python keyword ``in`` with a ``SeqFeature`` or location
object to see if the base/residue for a parent coordinate is within the
feature/location or not.

For example, suppose you have a SNP of interest and you want to know
which features this SNP is within, and lets suppose this SNP is at index
4350 (Python counting!). Here is a simple brute force solution where we
just check all the features one by one in a loop:

::

    >>> from Bio import SeqIO
    >>> my_snp = 4350
    >>> record = SeqIO.read("NC_005816.gb", "genbank")
    >>> for feature in record.features:
    ...     if my_snp in feature:
    ...         print("%s %s" % (feature.type, feature.qualifiers.get('db_xref')))
    ...
    source ['taxon:229193']
    gene ['GeneID:2767712']
    CDS ['GI:45478716', 'GeneID:2767712']

Note that gene and CDS features from GenBank or EMBL files defined with
joins are the union of the exons – they do not cover any introns.

Sequence described by a feature or location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``SeqFeature`` or location object doesn’t directly contain a sequence,
instead the location (see Section \ `3.2 <#sec:locations>`__) describes
how to get this from the parent sequence. For example consider a (short)
gene sequence with location 5:18 on the reverse strand, which in
GenBank/EMBL notation using 1-based counting would be
``complement(6..18)``, like this:

::

    >>> from Bio.Seq import Seq
    >>> from Bio.SeqFeature import SeqFeature, FeatureLocation
    >>> example_parent = Seq("ACCGAGACGGCAAAGGCTAGCATAGGTATGAGACTTCCTTCCTGCCAGTGCTGAGGAACTGGGAGCCTAC")
    >>> example_feature = SeqFeature(FeatureLocation(5, 18), type="gene", strand=-1)

You could take the parent sequence, slice it to extract 5:18, and then
take the reverse complement. If you are using Biopython 1.59 or later,
the feature location’s start and end are integer like so this works:

::

    >>> feature_seq = example_parent[example_feature.location.start:example_feature.location.end].reverse_complement()
    >>> print(feature_seq)
    AGCCTTTGCCGTC

This is a simple example so this isn’t too bad – however once you have
to deal with compound features (joins) this is rather messy. Instead,
the ``SeqFeature`` object has an ``extract`` method to take care of all
this:

::

    >>> feature_seq = example_feature.extract(example_parent)
    >>> print(feature_seq)
    AGCCTTTGCCGTC

The length of a ``SeqFeature`` or location matches that of the region of
sequence it describes.

::

    >>> print(example_feature.extract(example_parent))
    AGCCTTTGCCGTC
    >>> print(len(example_feature.extract(example_parent)))
    13
    >>> print(len(example_feature))
    13
    >>> print(len(example_feature.location))
    13

For simple ``FeatureLocation`` objects the length is just the difference
between the start and end positions. However, for a ``CompoundLocation``
the length is the sum of the constituent regions.

Comparison
----------

The ``SeqRecord`` objects can be very complex, but here’s a simple
example:

::

    >>> from Bio.Seq import Seq
    >>> from Bio.SeqRecord import SeqRecord
    >>> record1 = SeqRecord(Seq("ACGT"), id="test")
    >>> record2 = SeqRecord(Seq("ACGT"), id="test")

What happens when you try to compare these “identical” records?

::

    >>> record1 == record2
    ...

Perhaps surprisingly older versions of Biopython would use Python’s
default object comparison for the ``SeqRecord``, meaning
``record1 == record2`` would only return ``True`` if these variables
pointed at the same object in memory. In this example,
``record1 == record2`` would have returned ``False`` here!

::

    >>> record1 == record2  # on old versions of Biopython!
    False

As of Biopython 1.67, ``SeqRecord`` comparison like
``record1 == record2`` will instead raise an explicit error to avoid
people being caught out by this:

::

    >>> record1 == record2
    Traceback (most recent call last):
    ...
    NotImplementedError: SeqRecord comparison is deliberately not implemented. Explicitly compare the attributes of interest.

Instead you should check the attributes you are interested in, for
example the identifier and the sequence:

::

    >>> record1.id == record2.id
    True
    >>> record1.seq == record2.seq
    True

Beware that comparing complex objects quickly gets complicated (see also
Section \ `[sec:seq-comparison] <#sec:seq-comparison>`__).

References
----------

Another common annotation related to a sequence is a reference to a
journal or other published work dealing with the sequence. We have a
fairly simple way of representing a Reference in Biopython – we have a
``Bio.SeqFeature.Reference`` class that stores the relevant information
about a reference as attributes of an object.

The attributes include things that you would expect to see in a
reference like ``journal``, ``title`` and ``authors``. Additionally, it
also can hold the ``medline_id`` and ``pubmed_id`` and a ``comment``
about the reference. These are all accessed simply as attributes of the
object.

A reference also has a ``location`` object so that it can specify a
particular location on the sequence that the reference refers to. For
instance, you might have a journal that is dealing with a particular
gene located on a BAC, and want to specify that it only refers to this
position exactly. The ``location`` is a potentially fuzzy location, as
described in section \ `3.2 <#sec:locations>`__.

Any reference objects are stored as a list in the ``SeqRecord`` object’s
``annotations`` dictionary under the key “references”. That’s all there
is too it. References are meant to be easy to deal with, and hopefully
general enough to cover lots of usage cases.

.. sec:SeqRecord-format:

The format method
-----------------

The ``format()`` method of the ``SeqRecord`` class gives a string
containing your record formatted using one of the output file formats
supported by ``Bio.SeqIO``, such as FASTA:

::

    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio.Alphabet import generic_protein

    record = SeqRecord(Seq("MMYQQGCFAGGTVLRLAKDLAENNRGARVLVVCSEITAVTFRGPSETHLDSMVGQALFGD" \
                          +"GAGAVIVGSDPDLSVERPLYELVWTGATLLPDSEGAIDGHLREVGLTFHLLKDVPGLISK" \
                          +"NIEKSLKEAFTPLGISDWNSTFWIAHPGGPAILDQVEAKLGLKEEKMRATREVLSEYGNM" \
                          +"SSAC", generic_protein),
                       id="gi|14150838|gb|AAK54648.1|AF376133_1",
                       description="chalcone synthase [Cucumis sativus]")

    print(record.format("fasta"))

which should give:

::

    >gi|14150838|gb|AAK54648.1|AF376133_1 chalcone synthase [Cucumis sativus]
    MMYQQGCFAGGTVLRLAKDLAENNRGARVLVVCSEITAVTFRGPSETHLDSMVGQALFGD
    GAGAVIVGSDPDLSVERPLYELVWTGATLLPDSEGAIDGHLREVGLTFHLLKDVPGLISK
    NIEKSLKEAFTPLGISDWNSTFWIAHPGGPAILDQVEAKLGLKEEKMRATREVLSEYGNM
    SSAC

This ``format`` method takes a single mandatory argument, a lower case
string which is supported by ``Bio.SeqIO`` as an output format (see
Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__). However, some
of the file formats ``Bio.SeqIO`` can write to *require* more than one
record (typically the case for multiple sequence alignment formats), and
thus won’t work via this ``format()`` method. See also
Section \ `[sec:Bio.SeqIO-and-StringIO] <#sec:Bio.SeqIO-and-StringIO>`__.

.. sec:SeqRecord-slicing:

Slicing a SeqRecord
-------------------

You can slice a ``SeqRecord``, to give you a new ``SeqRecord`` covering
just part of the sequence. What is important here is that any per-letter
annotations are also sliced, and any features which fall completely
within the new sequence are preserved (with their locations adjusted).

For example, taking the same GenBank file used earlier:

::

    >>> from Bio import SeqIO
    >>> record = SeqIO.read("NC_005816.gb", "genbank")

::

    >>> record
    SeqRecord(seq=Seq('TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGG...CTG',
    IUPACAmbiguousDNA()), id='NC_005816.1', name='NC_005816',
    description='Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence',
    dbxrefs=['Project:58037'])

::

    >>> len(record)
    9609
    >>> len(record.features)
    41

For this example we’re going to focus in on the ``pim`` gene,
``YP_pPCP05``. If you have a look at the GenBank file directly you’ll
find this gene/CDS has location string ``4343..4780``, or in Python
counting ``4342:4780``. From looking at the file you can work out that
these are the twelfth and thirteenth entries in the file, so in Python
zero-based counting they are entries :math:`11` and :math:`12` in the
``features`` list:

::

    >>> print(record.features[20])
    type: gene
    location: [4342:4780](+)
    qualifiers:
        Key: db_xref, Value: ['GeneID:2767712']
        Key: gene, Value: ['pim']
        Key: locus_tag, Value: ['YP_pPCP05']
    <BLANKLINE>

::

    >>> print(record.features[21])
    type: CDS
    location: [4342:4780](+)
    qualifiers:
        Key: codon_start, Value: ['1']
        Key: db_xref, Value: ['GI:45478716', 'GeneID:2767712']
        Key: gene, Value: ['pim']
        Key: locus_tag, Value: ['YP_pPCP05']
        Key: note, Value: ['similar to many previously sequenced pesticin immunity ...']
        Key: product, Value: ['pesticin immunity protein']
        Key: protein_id, Value: ['NP_995571.1']
        Key: transl_table, Value: ['11']
        Key: translation, Value: ['MGGGMISKLFCLALIFLSSSGLAEKNTYTAKDILQNLELNTFGNSLSH...']

Let’s slice this parent record from 4300 to 4800 (enough to include the
``pim`` gene/CDS), and see how many features we get:

::

    >>> sub_record = record[4300:4800]

::

    >>> sub_record
    SeqRecord(seq=Seq('ATAAATAGATTATTCCAAATAATTTATTTATGTAAGAACAGGATGGGAGGGGGA...TTA',
    IUPACAmbiguousDNA()), id='NC_005816.1', name='NC_005816',
    description='Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence.',
    dbxrefs=[])

::

    >>> len(sub_record)
    500
    >>> len(sub_record.features)
    2

Our sub-record just has two features, the gene and CDS entries for
``YP_pPCP05``:

::

    >>> print(sub_record.features[0])
    type: gene
    location: [42:480](+)
    qualifiers:
        Key: db_xref, Value: ['GeneID:2767712']
        Key: gene, Value: ['pim']
        Key: locus_tag, Value: ['YP_pPCP05']
    <BLANKLINE>

::

    >>> print(sub_record.features[1])
    type: CDS
    location: [42:480](+)
    qualifiers:
        Key: codon_start, Value: ['1']
        Key: db_xref, Value: ['GI:45478716', 'GeneID:2767712']
        Key: gene, Value: ['pim']
        Key: locus_tag, Value: ['YP_pPCP05']
        Key: note, Value: ['similar to many previously sequenced pesticin immunity ...']
        Key: product, Value: ['pesticin immunity protein']
        Key: protein_id, Value: ['NP_995571.1']
        Key: transl_table, Value: ['11']
        Key: translation, Value: ['MGGGMISKLFCLALIFLSSSGLAEKNTYTAKDILQNLELNTFGNSLSH...']

Notice that their locations have been adjusted to reflect the new parent
sequence!

While Biopython has done something sensible and hopefully intuitive with
the features (and any per-letter annotation), for the other annotation
it is impossible to know if this still applies to the sub-sequence or
not. To avoid guessing, the ``annotations`` and ``dbxrefs`` are omitted
from the sub-record, and it is up to you to transfer any relevant
information as appropriate.

::

    >>> sub_record.annotations
    {}
    >>> sub_record.dbxrefs
    []

The same point could be made about the record ``id``, ``name`` and
``description``, but for practicality these are preserved:

::

    >>> sub_record.id
    'NC_005816.1'
    >>> sub_record.name
    'NC_005816'
    >>> sub_record.description
    'Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence'

This illustrates the problem nicely though, our new sub-record is *not*
the complete sequence of the plasmid, so the description is wrong! Let’s
fix this and then view the sub-record as a reduced GenBank file using
the ``format`` method described above in
Section \ `6 <#sec:SeqRecord-format>`__:

::

    >>> sub_record.description = "Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, partial."
    >>> print(sub_record.format("genbank"))
    ...

See
Sections \ `[sec:FASTQ-slicing-off-primer] <#sec:FASTQ-slicing-off-primer>`__
and \ `[sec:FASTQ-slicing-off-adaptor] <#sec:FASTQ-slicing-off-adaptor>`__
for some FASTQ examples where the per-letter annotations (the read
quality scores) are also sliced.

.. sec:SeqRecord-addition:

Adding SeqRecord objects
------------------------

You can add ``SeqRecord`` objects together, giving a new ``SeqRecord``.
What is important here is that any common per-letter annotations are
also added, all the features are preserved (with their locations
adjusted), and any other common annotation is also kept (like the id,
name and description).

For an example with per-letter annotation, we’ll use the first record in
a FASTQ file. Chapter \ `[chapter:Bio.SeqIO] <#chapter:Bio.SeqIO>`__
will explain the ``SeqIO`` functions:

::

    >>> from Bio import SeqIO
    >>> record = next(SeqIO.parse("example.fastq", "fastq"))
    >>> len(record)
    25
    >>> print(record.seq)
    CCCTTCTTGTCTTCAGCGTTTCTCC

::

    >>> print(record.letter_annotations["phred_quality"])
    [26, 26, 18, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 22, 26, 26, 26, 26,
    26, 26, 26, 23, 23]

Let’s suppose this was Roche 454 data, and that from other information
you think the ``TTT`` should be only ``TT``. We can make a new edited
record by first slicing the ``SeqRecord`` before and after the “extra”
third ``T``:

::

    >>> left = record[:20]
    >>> print(left.seq)
    CCCTTCTTGTCTTCAGCGTT
    >>> print(left.letter_annotations["phred_quality"])
    [26, 26, 18, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 22, 26, 26, 26, 26]
    >>> right = record[21:]
    >>> print(right.seq)
    CTCC
    >>> print(right.letter_annotations["phred_quality"])
    [26, 26, 23, 23]

Now add the two parts together:

::

    >>> edited = left + right
    >>> len(edited)
    24
    >>> print(edited.seq)
    CCCTTCTTGTCTTCAGCGTTCTCC

::

    >>> print(edited.letter_annotations["phred_quality"])
    [26, 26, 18, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 22, 26, 26, 26, 26,
    26, 26, 23, 23]

Easy and intuitive? We hope so! You can make this shorter with just:

::

    >>> edited = record[:20] + record[21:]

Now, for an example with features, we’ll use a GenBank file. Suppose you
have a circular genome:

::

    >>> from Bio import SeqIO
    >>> record = SeqIO.read("NC_005816.gb", "genbank")

::

    >>> record
    SeqRecord(seq=Seq('TGTAACGAACGGTGCAATAGTGATCCACACCCAACGCCTGAAATCAGATCCAGG...CTG',
    IUPACAmbiguousDNA()), id='NC_005816.1', name='NC_005816',
    description='Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence.',
    dbxrefs=['Project:10638'])

::

    >>> len(record)
    9609
    >>> len(record.features)
    41
    >>> record.dbxrefs
    ['Project:58037']

::

    >>> record.annotations.keys()
    ['comment', 'sequence_version', 'source', 'taxonomy', 'keywords', 'references',
    'accessions', 'data_file_division', 'date', 'organism', 'gi']

You can shift the origin like this:

::

    >>> shifted = record[2000:] + record[:2000]

::

    >>> shifted
    SeqRecord(seq=Seq('GATACGCAGTCATATTTTTTACACAATTCTCTAATCCCGACAAGGTCGTAGGTC...GGA',
    IUPACAmbiguousDNA()), id='NC_005816.1', name='NC_005816',
    description='Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1, complete sequence.',
    dbxrefs=[])

::

    >>> len(shifted)
    9609

Note that this isn’t perfect in that some annotation like the database
cross references and one of the features (the source feature) have been
lost:

::

    >>> len(shifted.features)
    40
    >>> shifted.dbxrefs
    []
    >>> shifted.annotations.keys()
    []

This is because the ``SeqRecord`` slicing step is cautious in what
annotation it preserves (erroneously propagating annotation can cause
major problems). If you want to keep the database cross references or
the annotations dictionary, this must be done explicitly:

::

    >>> shifted.dbxrefs = record.dbxrefs[:]
    >>> shifted.annotations = record.annotations.copy()
    >>> shifted.dbxrefs
    ['Project:10638']
    >>> shifted.annotations.keys()
    ['comment', 'sequence_version', 'source', 'taxonomy', 'keywords', 'references',
    'accessions', 'data_file_division', 'date', 'organism', 'gi']

Also note that in an example like this, you should probably change the
record identifiers since the NCBI references refer to the *original*
unmodified sequence.

.. sec:SeqRecord-reverse-complement:

Reverse-complementing SeqRecord objects
---------------------------------------

One of the new features in Biopython 1.57 was the ``SeqRecord`` object’s
``reverse_complement`` method. This tries to balance easy of use with
worries about what to do with the annotation in the reverse complemented
record.

For the sequence, this uses the Seq object’s reverse complement method.
Any features are transferred with the location and strand recalculated.
Likewise any per-letter-annotation is also copied but reversed (which
makes sense for typical examples like quality scores). However, transfer
of most annotation is problematical.

For instance, if the record ID was an accession, that accession should
not really apply to the reverse complemented sequence, and transferring
the identifier by default could easily cause subtle data corruption in
downstream analysis. Therefore by default, the ``SeqRecord``\ ’s id,
name, description, annotations and database cross references are all
*not* transferred by default.

The ``SeqRecord`` object’s ``reverse_complement`` method takes a number
of optional arguments corresponding to properties of the record. Setting
these arguments to ``True`` means copy the old values, while ``False``
means drop the old values and use the default value. You can
alternatively provide the new desired value instead.

Consider this example record:

::

    >>> from Bio import SeqIO
    >>> record = SeqIO.read("NC_005816.gb", "genbank")
    >>> print("%s %i %i %i %i" % (record.id, len(record), len(record.features), len(record.dbxrefs), len(record.annotations)))
    NC_005816.1 9609 41 1 13

Here we take the reverse complement and specify a new identifier – but
notice how most of the annotation is dropped (but not the features):

::

    >>> rc = record.reverse_complement(id="TESTING")
    >>> print("%s %i %i %i %i" % (rc.id, len(rc), len(rc.features), len(rc.dbxrefs), len(rc.annotations)))
    TESTING 9609 41 0 0
