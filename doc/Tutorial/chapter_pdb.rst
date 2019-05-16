Going 3D: The PDB module
========================

Bio.PDB is a Biopython module that focuses on working with crystal
structures of biological macromolecules. Among other things, Bio.PDB
includes a PDBParser class that produces a Structure object, which can
be used to access the atomic data in the file in a convenient manner.
There is limited support for parsing the information contained in the
PDB header.

Reading and writing crystal structure files
-------------------------------------------

Reading a PDB file
~~~~~~~~~~~~~~~~~~

First we create a ``PDBParser`` object:

::

    >>> from Bio.PDB.PDBParser import PDBParser
    >>> parser = PDBParser(PERMISSIVE=1)

The PERMISSIVE flag indicates that a number of common problems (see
`[problem structures] <#problem structures>`__) associated with PDB
files will be ignored (but note that some atoms and/or residues will be
missing). If the flag is not present a PDBConstructionException will be
generated if any problems are detected during the parse operation.

The Structure object is then produced by letting the ``PDBParser``
object parse a PDB file (the PDB file in this case is called
``pdb1fat.ent``, ``1fat`` is a user defined name for the structure):

::

    >>> structure_id = "1fat"
    >>> filename = "pdb1fat.ent"
    >>> structure = parser.get_structure(structure_id, filename)

You can extract the header and trailer (simple lists of strings) of the
PDB file from the PDBParser object with the get_header and get_trailer
methods. Note however that many PDB files contain headers with
incomplete or erroneous information. Many of the errors have been fixed
in the equivalent mmCIF files. *Hence, if you are interested in the
header information, it is a good idea to extract information from mmCIF
files using the* ``MMCIF2Dict`` *tool described below, instead of
parsing the PDB header.*

Now that is clarified, let’s return to parsing the PDB header. The
structure object has an attribute called ``header`` which is a Python
dictionary that maps header records to their values.

Example:

::

    >>> resolution = structure.header['resolution']
    >>> keywords = structure.header['keywords']

The available keys are ``name``, ``head``, ``deposition_date``,
``release_date``, ``structure_method``, ``resolution``,
``structure_reference`` (which maps to a list of references),
``journal_reference``, ``author``, and ``compound`` (which maps to a
dictionary with various information about the crystallized compound).

The dictionary can also be created without creating a ``Structure``
object, ie. directly from the PDB file:

::

    >>> from Bio.PDB import parse_pdb_header
    >>> with open(filename, 'r') as handle:
    ...     header_dict = parse_pdb_header(handle)
    ...

Reading an mmCIF file
~~~~~~~~~~~~~~~~~~~~~

Similarly to the case of PDB files, first create an ``MMCIFParser``
object:

::

    >>> from Bio.PDB.MMCIFParser import MMCIFParser
    >>> parser = MMCIFParser()

Then use this parser to create a structure object from the mmCIF file:

::

    >>> structure = parser.get_structure('1fat', '1fat.cif')

To have some more low level access to an mmCIF file, you can use the
``MMCIF2Dict`` class to create a Python dictionary that maps all mmCIF
tags in an mmCIF file to their values. If there are multiple values
(like in the case of tag ``_atom_site.Cartn_y``, which holds the
:math:`y` coordinates of all atoms), the tag is mapped to a list of
values. The dictionary is created from the mmCIF file as follows:

::

    >>> from Bio.PDB.MMCIF2Dict import MMCIF2Dict
    >>> mmcif_dict = MMCIF2Dict('1FAT.cif')

Example: get the solvent content from an mmCIF file:

::

    >>> sc = mmcif_dict['_exptl_crystal.density_percent_sol']

Example: get the list of the :math:`y` coordinates of all atoms

::

    >>> y_list = mmcif_dict['_atom_site.Cartn_y']

Reading files in the MMTF format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the direct MMTFParser to read a structure from a file:

::

    >>> from Bio.PDB.mmtf import MMTFParser
    >>> structure = MMTFParser.get_structure("PDB/4CUP.mmtf")

Or you can use the same class to get a structure by its PDB ID:

::

    >>> structure = MMTFParser.get_structure_from_url("4CUP")

This gives you a Structure object as if read from a PDB or mmCIF file.

You can also have access to the underlying data using the external MMTF
library which Biopython is using internally:

::

    >>> from mmtf import fetch
    >>> decoded_data = fetch("4CUP")

For example you can access just the X-coordinate.

::

    >>> print(decoded_data.x_coord_list)
    ...

Reading files in the PDB XML format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

That’s not yet supported, but we are definitely planning to support that
in the future (it’s not a lot of work). Contact the Biopython developers
() if you need this).

Writing PDB files
~~~~~~~~~~~~~~~~~

Use the PDBIO class for this. It’s easy to write out specific parts of a
structure too, of course.

Example: saving a structure

::

    >>> io = PDBIO()
    >>> io.set_structure(s)
    >>> io.save('out.pdb')

If you want to write out a part of the structure, make use of the
``Select`` class (also in ``PDBIO``). Select has four methods:

-  ``accept_model(model)``

-  ``accept_chain(chain)``

-  ``accept_residue(residue)``

-  ``accept_atom(atom)``

By default, every method returns 1 (which means the
model/chain/residue/atom is included in the output). By subclassing
``Select`` and returning 0 when appropriate you can exclude models,
chains, etc. from the output. Cumbersome maybe, but very powerful. The
following code only writes out glycine residues:

::

    >>> class GlySelect(Select):
    ...     def accept_residue(self, residue):
    ...         if residue.get_name()=='GLY':
    ...             return True
    ...         else:
    ...             return False
    ...
    >>> io = PDBIO()
    >>> io.set_structure(s)
    >>> io.save('gly_only.pdb', GlySelect())

If this is all too complicated for you, the ``Dice`` module contains a
handy ``extract`` function that writes out all residues in a chain
between a start and end residue.

Writing mmCIF files
~~~~~~~~~~~~~~~~~~~

A similar interface can be used to write structures to the mmCIF file
format:

::

    >>> io = MMCIFIO()
    >>> io.set_structure(s)
    >>> io.save('out.cif')

The ``Select`` class can be used in a similar way to ``PDBIO`` above.
mmCIF dictionaries read using ``MMCIF2Dict`` can also be written:

::

    >>> io = MMCIFIO()
    >>> io.set_dict(d)
    >>> io.save('out.cif')

Structure representation
------------------------

The overall layout of a ``Structure`` object follows the so-called SMCRA
(Structure/Model/Chain/Residue/Atom) architecture:

-  A structure consists of models

-  A model consists of chains

-  A chain consists of residues

-  A residue consists of atoms

This is the way many structural biologists/bioinformaticians think about
structure, and provides a simple but efficient way to deal with
structure. Additional stuff is essentially added when needed. A UML
diagram of the ``Structure`` object (forget about the ``Disordered``
classes for now) is shown in Fig. `[fig:smcra] <#fig:smcra>`__. Such a
data structure is not necessarily best suited for the representation of
the macromolecular content of a structure, but it is absolutely
necessary for a good interpretation of the data present in a file that
describes the structure (typically a PDB or MMCIF file). If this
hierarchy cannot represent the contents of a structure file, it is
fairly certain that the file contains an error or at least does not
describe the structure unambiguously. If a SMCRA data structure cannot
be generated, there is reason to suspect a problem. Parsing a PDB file
can thus be used to detect likely problems. We will give several
examples of this in section
`[problem structures] <#problem structures>`__.

.. raw:: latex

   \imgsrc[width=650, height=750]{images/smcra.png}

.. raw:: latex

   \centering

.. figure:: images/smcra.png
   :alt: UML diagram of SMCRA architecture of the ``Structure`` class
   used to represent a macromolecular structure. Full lines with
   diamonds denote aggregation, full lines with arrows denote
   referencing, full lines with triangles denote inheritance and dashed
   lines with triangles denote interface realization.
   :width: 80.0%

   UML diagram of SMCRA architecture of the ``Structure`` class used to
   represent a macromolecular structure. Full lines with diamonds denote
   aggregation, full lines with arrows denote referencing, full lines
   with triangles denote inheritance and dashed lines with triangles
   denote interface realization.

Structure, Model, Chain and Residue are all subclasses of the Entity
base class. The Atom class only (partly) implements the Entity interface
(because an Atom does not have children).

For each Entity subclass, you can extract a child by using a unique id
for that child as a key (e.g. you can extract an Atom object from a
Residue object by using an atom name string as a key, you can extract a
Chain object from a Model object by using its chain identifier as a
key).

Disordered atoms and residues are represented by DisorderedAtom and
DisorderedResidue classes, which are both subclasses of the
DisorderedEntityWrapper base class. They hide the complexity associated
with disorder and behave exactly as Atom and Residue objects.

In general, a child Entity object (i.e. Atom, Residue, Chain, Model) can
be extracted from its parent (i.e. Residue, Chain, Model, Structure,
respectively) by using an id as a key.

::

    >>> child_entity = parent_entity[child_id]

You can also get a list of all child Entities of a parent Entity object.
Note that this list is sorted in a specific way (e.g. according to chain
identifier for Chain objects in a Model object).

::

    >>> child_list = parent_entity.get_list()

You can also get the parent from a child:

::

    >>> parent_entity = child_entity.get_parent()

At all levels of the SMCRA hierarchy, you can also extract a *full id*.
The full id is a tuple containing all id’s starting from the top object
(Structure) down to the current object. A full id for a Residue object
e.g. is something like:

::

    >>> full_id = residue.get_full_id()
    >>> print(full_id)
    ("1abc", 0, "A", ("", 10, "A"))

This corresponds to:

-  The Structure with id ‘̈1abc‘̈

-  The Model with id 0

-  The Chain with id ‘̈A‘̈

-  The Residue with id (‘̈ ‘̈, 10, ‘̈A‘̈).

The Residue id indicates that the residue is not a hetero-residue (nor a
water) because it has a blank hetero field, that its sequence identifier
is 10 and that its insertion code is ‘̈A‘̈.

To get the entity’s id, use the ``get_id`` method:

::

    >>> entity.get_id()

You can check if the entity has a child with a given id by using the
``has_id`` method:

::

    >>> entity.has_id(entity_id)

The length of an entity is equal to its number of children:

::

    >>> nr_children = len(entity)

It is possible to delete, rename, add, etc. child entities from a parent
entity, but this does not include any sanity checks (e.g. it is possible
to add two residues with the same id to one chain). This really should
be done via a nice Decorator class that includes integrity checking, but
you can take a look at the code (Entity.py) if you want to use the raw
interface.

Structure
~~~~~~~~~

The Structure object is at the top of the hierarchy. Its id is a user
given string. The Structure contains a number of Model children. Most
crystal structures (but not all) contain a single model, while NMR
structures typically consist of several models. Disorder in crystal
structures of large parts of molecules can also result in several
models.

Model
~~~~~

The id of the Model object is an integer, which is derived from the
position of the model in the parsed file (they are automatically
numbered starting from 0). Crystal structures generally have only one
model (with id 0), while NMR files usually have several models. Whereas
many PDB parsers assume that there is only one model, the ``Structure``
class in ``Bio.PDB`` is designed such that it can easily handle PDB
files with more than one model.

As an example, to get the first model from a Structure object, use

::

    >>> first_model = structure[0]

The Model object stores a list of Chain children.

Chain
~~~~~

The id of a Chain object is derived from the chain identifier in the
PDB/mmCIF file, and is a single character (typically a letter). Each
Chain in a Model object has a unique id. As an example, to get the Chain
object with identifier “A” from a Model object, use

::

    >>> chain_A = model["A"]

The Chain object stores a list of Residue children.

Residue
~~~~~~~

A residue id is a tuple with three elements:

-  The **hetero-field** (hetfield): this is

   -  ``'W'`` in the case of a water molecule;

   -  ``'H_'`` followed by the residue name for other hetero residues
      (e.g. ``'H_GLC'`` in the case of a glucose molecule);

   -  blank for standard amino and nucleic acids.

   This scheme is adopted for reasons described in section
   `[hetero problems] <#hetero problems>`__.

-  The **sequence identifier** (resseq), an integer describing the
   position of the residue in the chain (e.g., 100);

-  The **insertion code** (icode); a string, e.g. ’A’. The insertion
   code is sometimes used to preserve a certain desirable residue
   numbering scheme. A Ser 80 insertion mutant (inserted e.g. between a
   Thr 80 and an Asn 81 residue) could e.g. have sequence identifiers
   and insertion codes as follows: Thr 80 A, Ser 80 B, Asn 81. In this
   way the residue numbering scheme stays in tune with that of the wild
   type structure.

The id of the above glucose residue would thus be
``(’H_GLC’, 100, ’A’)``. If the hetero-flag and insertion code are
blank, the sequence identifier alone can be used:

::

    # Full id
    >>> residue=chain[(' ', 100, ' ')]
    # Shortcut id
    >>> residue=chain[100]

The reason for the hetero-flag is that many, many PDB files use the same
sequence identifier for an amino acid and a hetero-residue or a water,
which would create obvious problems if the hetero-flag was not used.

Unsurprisingly, a Residue object stores a set of Atom children. It also
contains a string that specifies the residue name (e.g. “ASN”) and the
segment identifier of the residue (well known to X-PLOR users, but not
used in the construction of the SMCRA data structure).

Let’s look at some examples. Asn 10 with a blank insertion code would
have residue id (’ ’, 10, ’ ’). Water 10 would have residue id (’W’, 10,
’ ’). A glucose molecule (a hetero residue with residue name GLC) with
sequence identifier 10 would have residue id (’H_GLC’, 10, ’ ’). In this
way, the three residues (with the same insertion code and sequence
identifier) can be part of the same chain because their residue id’s are
distinct.

In most cases, the hetflag and insertion code fields will be blank, e.g.
(’ ’, 10, ’ ’). In these cases, the sequence identifier can be used as a
shortcut for the full id:

::

    # use full id
    >>> res10 = chain[(' ', 10, ' ')]
    # use shortcut
    >>> res10 = chain[10]

Each Residue object in a Chain object should have a unique id. However,
disordered residues are dealt with in a special way, as described in
section `[point mutations] <#point mutations>`__.

A Residue object has a number of additional methods:

::

    >>> residue.get_resname()       # returns the residue name, e.g. "ASN"
    >>> residue.is_disordered()     # returns 1 if the residue has disordered atoms
    >>> residue.get_segid()         # returns the SEGID, e.g. "CHN1"
    >>> residue.has_id(name)        # test if a residue has a certain atom

You can use ``is_aa(residue)`` to test if a Residue object is an amino
acid.

Atom
~~~~

The Atom object stores the data associated with an atom, and has no
children. The id of an atom is its atom name (e.g. “OG” for the side
chain oxygen of a Ser residue). An Atom id needs to be unique in a
Residue. Again, an exception is made for disordered atoms, as described
in section `[disordered atoms] <#disordered atoms>`__.

The atom id is simply the atom name (eg. ``’CA’``). In practice, the
atom name is created by stripping all spaces from the atom name in the
PDB file.

However, in PDB files, a space can be part of an atom name. Often,
calcium atoms are called ``’CA..’`` in order to distinguish them from
C\ :math:`\alpha` atoms (which are called ``’.CA.’``). In cases were
stripping the spaces would create problems (ie. two atoms called
``’CA’`` in the same residue) the spaces are kept.

In a PDB file, an atom name consists of 4 chars, typically with leading
and trailing spaces. Often these spaces can be removed for ease of use
(e.g. an amino acid C\ :math:`\alpha` atom is labeled “.CA.” in a PDB
file, where the dots represent spaces). To generate an atom name (and
thus an atom id) the spaces are removed, unless this would result in a
name collision in a Residue (i.e. two Atom objects with the same atom
name and id). In the latter case, the atom name including spaces is
tried. This situation can e.g. happen when one residue contains atoms
with names “.CA.” and “CA..”, although this is not very likely.

The atomic data stored includes the atom name, the atomic coordinates
(including standard deviation if present), the B factor (including
anisotropic B factors and standard deviation if present), the altloc
specifier and the full atom name including spaces. Less used items like
the atom element number or the atomic charge sometimes specified in a
PDB file are not stored.

To manipulate the atomic coordinates, use the ``transform`` method of
the ``Atom`` object. Use the ``set_coord`` method to specify the atomic
coordinates directly.

An Atom object has the following additional methods:

::

    >>> a.get_name()       # atom name (spaces stripped, e.g. "CA")
    >>> a.get_id()         # id (equals atom name)
    >>> a.get_coord()      # atomic coordinates
    >>> a.get_vector()     # atomic coordinates as Vector object
    >>> a.get_bfactor()    # isotropic B factor
    >>> a.get_occupancy()  # occupancy
    >>> a.get_altloc()     # alternative location specifier
    >>> a.get_sigatm()     # standard deviation of atomic parameters
    >>> a.get_siguij()     # standard deviation of anisotropic B factor
    >>> a.get_anisou()     # anisotropic B factor
    >>> a.get_fullname()   # atom name (with spaces, e.g. ".CA.")

To represent the atom coordinates, siguij, anisotropic B factor and
sigatm Numpy arrays are used.

The ``get_vector`` method returns a ``Vector`` object representation of
the coordinates of the ``Atom`` object, allowing you to do vector
operations on atomic coordinates. ``Vector`` implements the full set of
3D vector operations, matrix multiplication (left and right) and some
advanced rotation-related operations as well.

As an example of the capabilities of Bio.PDB’s ``Vector`` module,
suppose that you would like to find the position of a Gly residue’s
C\ :math:`\beta` atom, if it had one. Rotating the N atom of the Gly
residue along the C\ :math:`\alpha`-C bond over -120 degrees roughly
puts it in the position of a virtual C\ :math:`\beta` atom. Here’s how
to do it, making use of the ``rotaxis`` method (which can be used to
construct a rotation around a certain axis) of the ``Vector`` module:

::

    # get atom coordinates as vectors
    >>> n = residue['N'].get_vector()
    >>> c = residue['C'].get_vector()
    >>> ca = residue['CA'].get_vector()
    # center at origin
    >>> n = n - ca
    >>> c = c - ca
    # find rotation matrix that rotates n
    # -120 degrees along the ca-c vector
    >>> rot = rotaxis(-pi * 120.0/180.0, c)
    # apply rotation to ca-n vector
    >>> cb_at_origin = n.left_multiply(rot)
    # put on top of ca atom
    >>> cb = cb_at_origin+ca

This example shows that it’s possible to do some quite nontrivial vector
operations on atomic data, which can be quite useful. In addition to all
the usual vector operations (cross (use ``**``), and dot (use ``*``)
product, angle, norm, etc.) and the above mentioned ``rotaxis``
function, the ``Vector`` module also has methods to rotate (``rotmat``)
or reflect (``refmat``) one vector on top of another.

Extracting a specific ``Atom/Residue/Chain/Model`` from a Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are some examples:

::

    >>> model = structure[0]
    >>> chain = model['A']
    >>> residue = chain[100]
    >>> atom = residue['CA']

Note that you can use a shortcut:

::

    >>> atom = structure[0]['A'][100]['CA']

Disorder
--------

Bio.PDB can handle both disordered atoms and point mutations (i.e. a Gly
and an Ala residue in the same position).

General approach[disorder problems]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Disorder should be dealt with from two points of view: the atom and the
residue points of view. In general, we have tried to encapsulate all the
complexity that arises from disorder. If you just want to loop over all
C\ :math:`\alpha` atoms, you do not care that some residues have a
disordered side chain. On the other hand it should also be possible to
represent disorder completely in the data structure. Therefore,
disordered atoms or residues are stored in special objects that behave
as if there is no disorder. This is done by only representing a subset
of the disordered atoms or residues. Which subset is picked (e.g. which
of the two disordered OG side chain atom positions of a Ser residue is
used) can be specified by the user.

Disordered atoms[disordered atoms]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Disordered atoms are represented by ordinary ``Atom`` objects, but all
``Atom`` objects that represent the same physical atom are stored in a
``DisorderedAtom`` object (see Fig. `[fig:smcra] <#fig:smcra>`__). Each
``Atom`` object in a ``DisorderedAtom`` object can be uniquely indexed
using its altloc specifier. The ``DisorderedAtom`` object forwards all
uncaught method calls to the selected Atom object, by default the one
that represents the atom with the highest occupancy. The user can of
course change the selected ``Atom`` object, making use of its altloc
specifier. In this way atom disorder is represented correctly without
much additional complexity. In other words, if you are not interested in
atom disorder, you will not be bothered by it.

Each disordered atom has a characteristic altloc identifier. You can
specify that a ``DisorderedAtom`` object should behave like the ``Atom``
object associated with a specific altloc identifier:

::

    >>> atom.disordered_select('A') # select altloc A atom
    >>> print(atom.get_altloc())
    "A"
    >>> atom.disordered_select('B') # select altloc B atom
    >>> print(atom.get_altloc())
    "B"

Disordered residues
~~~~~~~~~~~~~~~~~~~

Common case
^^^^^^^^^^^

The most common case is a residue that contains one or more disordered
atoms. This is evidently solved by using DisorderedAtom objects to
represent the disordered atoms, and storing the DisorderedAtom object in
a Residue object just like ordinary Atom objects. The DisorderedAtom
will behave exactly like an ordinary atom (in fact the atom with the
highest occupancy) by forwarding all uncaught method calls to one of the
Atom objects (the selected Atom object) it contains.

Point mutations[point mutations]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A special case arises when disorder is due to a point mutation, i.e.
when two or more point mutants of a polypeptide are present in the
crystal. An example of this can be found in PDB structure 1EN2.

Since these residues belong to a different residue type (e.g. let’s say
Ser 60 and Cys 60) they should not be stored in a single ``Residue``
object as in the common case. In this case, each residue is represented
by one ``Residue`` object, and both ``Residue`` objects are stored in a
single ``DisorderedResidue`` object (see Fig.
`[fig:smcra] <#fig:smcra>`__).

The ``DisorderedResidue`` object forwards all uncaught methods to the
selected ``Residue`` object (by default the last ``Residue`` object
added), and thus behaves like an ordinary residue. Each ``Residue``
object in a ``DisorderedResidue`` object can be uniquely identified by
its residue name. In the above example, residue Ser 60 would have id
“SER” in the ``DisorderedResidue`` object, while residue Cys 60 would
have id “CYS”. The user can select the active ``Residue`` object in a
``DisorderedResidue`` object via this id.

Example: suppose that a chain has a point mutation at position 10,
consisting of a Ser and a Cys residue. Make sure that residue 10 of this
chain behaves as the Cys residue.

::

    >>> residue = chain[10]
    >>> residue.disordered_select('CYS')

In addition, you can get a list of all ``Atom`` objects (ie. all
``DisorderedAtom`` objects are ’unpacked’ to their individual ``Atom``
objects) using the ``get_unpacked_list`` method of a
``(Disordered)Residue`` object.

Hetero residues
---------------

Associated problems[hetero problems]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A common problem with hetero residues is that several hetero and
non-hetero residues present in the same chain share the same sequence
identifier (and insertion code). Therefore, to generate a unique id for
each hetero residue, waters and other hetero residues are treated in a
different way.

Remember that Residue object have the tuple (hetfield, resseq, icode) as
id. The hetfield is blank (“ ”) for amino and nucleic acids, and a
string for waters and other hetero residues. The content of the hetfield
is explained below.

Water residues
~~~~~~~~~~~~~~

The hetfield string of a water residue consists of the letter “W”. So a
typical residue id for a water is (“W”, 1, “ ”).

Other hetero residues
~~~~~~~~~~~~~~~~~~~~~

The hetfield string for other hetero residues starts with “H\_” followed
by the residue name. A glucose molecule e.g. with residue name “GLC”
would have hetfield “H_GLC”. Its residue id could e.g. be (“H_GLC”, 1, “
”).

Navigating through a Structure object
-------------------------------------

Parse a PDB file, and extract some Model, Chain, Residue and Atom objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> from Bio.PDB.PDBParser import PDBParser
    >>> parser = PDBParser()
    >>> structure = parser.get_structure("test", "1fat.pdb")
    >>> model = structure[0]
    >>> chain = model["A"]
    >>> residue = chain[1]
    >>> atom = residue["CA"]

Iterating through all atoms of a structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> p = PDBParser()
    >>> structure = p.get_structure('X', 'pdb1fat.ent')
    >>> for model in structure:
    ...     for chain in model:
    ...         for residue in chain:
    ...             for atom in residue:
    ...                 print(atom)
    ...

There is a shortcut if you want to iterate over all atoms in a
structure:

::

    >>> atoms = structure.get_atoms()
    >>> for atom in atoms:
    ...     print(atom)
    ...

Similarly, to iterate over all atoms in a chain, use

::

    >>> atoms = chain.get_atoms()
    >>> for atom in atoms:
    ...     print(atom)
    ...

Iterating over all residues of a model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

or if you want to iterate over all residues in a model:

::

    >>> residues = model.get_residues()
    >>> for residue in residues:
    ...     print(residue)
    ...

You can also use the ``Selection.unfold_entities`` function to get all
residues from a structure:

::

    >>> res_list = Selection.unfold_entities(structure, 'R')

or to get all atoms from a chain:

::

    >>> atom_list = Selection.unfold_entities(chain, 'A')

Obviously, ``A=atom, R=residue, C=chain, M=model, S=structure``. You can
use this to go up in the hierarchy, e.g. to get a list of (unique)
``Residue`` or ``Chain`` parents from a list of ``Atoms``:

::

    >>> residue_list = Selection.unfold_entities(atom_list, 'R')
    >>> chain_list = Selection.unfold_entities(atom_list, 'C')

For more info, see the API documentation.

Extract a hetero residue from a chain (e.g. a glucose (GLC) moiety with resseq 10)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> residue_id = ("H_GLC", 10, " ")
    >>> residue = chain[residue_id]

Print all hetero residues in chain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> for residue in chain.get_list():
    ...    residue_id = residue.get_id()
    ...    hetfield = residue_id[0]
    ...    if hetfield[0]=="H":
    ...        print(residue_id)
    ...

Print out the coordinates of all CA atoms in a structure with B factor greater than 50
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> for model in structure.get_list():
    ...     for chain in model.get_list():
    ...         for residue in chain.get_list():
    ...             if residue.has_id("CA"):
    ...                 ca = residue["CA"]
    ...                 if ca.get_bfactor() > 50.0:
    ...                     print(ca.get_coord())
    ...

Print out all the residues that contain disordered atoms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> for model in structure.get_list():
    ...     for chain in model.get_list():
    ...         for residue in chain.get_list():
    ...             if residue.is_disordered():
    ...                 resseq = residue.get_id()[1]
    ...                 resname = residue.get_resname()
    ...                 model_id = model.get_id()
    ...                 chain_id = chain.get_id()
    ...                 print(model_id, chain_id, resname, resseq)
    ...

Loop over all disordered atoms, and select all atoms with altloc A (if present)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will make sure that the SMCRA data structure will behave as if only
the atoms with altloc A are present.

::

    >>> for model in structure.get_list():
    ...     for chain in model.get_list():
    ...         for residue in chain.get_list():
    ...             if residue.is_disordered():
    ...                 for atom in residue.get_list():
    ...                     if atom.is_disordered():
    ...                         if atom.disordered_has_id("A"):
    ...                             atom.disordered_select("A")
    ...

Extracting polypeptides from a ``Structure`` object[subsubsec:extracting_polypeptides]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To extract polypeptides from a structure, construct a list of
``Polypeptide`` objects from a ``Structure`` object using
``PolypeptideBuilder`` as follows:

::

    >>> model_nr = 1
    >>> polypeptide_list = build_peptides(structure, model_nr)
    >>> for polypeptide in polypeptide_list:
    ...     print(polypeptide)
    ...

A Polypeptide object is simply a UserList of Residue objects, and is
always created from a single Model (in this case model 1). You can use
the resulting ``Polypeptide`` object to get the sequence as a ``Seq``
object or to get a list of C\ :math:`\alpha` atoms as well. Polypeptides
can be built using a C-N or a C\ :math:`\alpha`-C:math:`\alpha` distance
criterion.

Example:

::

    # Using C-N
    >>> ppb=PPBuilder()
    >>> for pp in ppb.build_peptides(structure):
    ...     print(pp.get_sequence())
    ...
    # Using CA-CA
    >>> ppb=CaPPBuilder()
    >>> for pp in ppb.build_peptides(structure):
    ...     print(pp.get_sequence())
    ...

Note that in the above case only model 0 of the structure is considered
by ``PolypeptideBuilder``. However, it is possible to use
``PolypeptideBuilder`` to build ``Polypeptide`` objects from ``Model``
and ``Chain`` objects as well.

Obtaining the sequence of a structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first thing to do is to extract all polypeptides from the structure
(as above). The sequence of each polypeptide can then easily be obtained
from the ``Polypeptide`` objects. The sequence is represented as a
Biopython ``Seq`` object, and its alphabet is defined by a
``ProteinAlphabet`` object.

Example:

::

    >>> seq = polypeptide.get_sequence()
    >>> print(seq)
    Seq('SNVVE...', <class Bio.Alphabet.ProteinAlphabet>)

Analyzing structures
--------------------

Measuring distances
~~~~~~~~~~~~~~~~~~~

The minus operator for atoms has been overloaded to return the distance
between two atoms.

::

    # Get some atoms
    >>> ca1 = residue1['CA']
    >>> ca2 = residue2['CA']
    # Simply subtract the atoms to get their distance
    >>> distance = ca1-ca2

Measuring angles
~~~~~~~~~~~~~~~~

Use the vector representation of the atomic coordinates, and the
``calc_angle`` function from the ``Vector`` module:

::

    >>> vector1 = atom1.get_vector()
    >>> vector2 = atom2.get_vector()
    >>> vector3 = atom3.get_vector()
    >>> angle = calc_angle(vector1, vector2, vector3)

Measuring torsion angles
~~~~~~~~~~~~~~~~~~~~~~~~

Use the vector representation of the atomic coordinates, and the
``calc_dihedral`` function from the ``Vector`` module:

::

    >>> vector1 = atom1.get_vector()
    >>> vector2 = atom2.get_vector()
    >>> vector3 = atom3.get_vector()
    >>> vector4 = atom4.get_vector()
    >>> angle = calc_dihedral(vector1, vector2, vector3, vector4)

Determining atom-atom contacts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``NeighborSearch`` to perform neighbor lookup. The neighbor lookup
is done using a KD tree module written in C (see ``Bio.KDTree``), making
it very fast. It also includes a fast method to find all point pairs
within a certain distance of each other.

Superimposing two structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use a ``Superimposer`` object to superimpose two coordinate sets. This
object calculates the rotation and translation matrix that rotates two
lists of atoms on top of each other in such a way that their RMSD is
minimized. Of course, the two lists need to contain the same number of
atoms. The ``Superimposer`` object can also apply the
rotation/translation to a list of atoms. The rotation and translation
are stored as a tuple in the ``rotran`` attribute of the
``Superimposer`` object (note that the rotation is right multiplying!).
The RMSD is stored in the ``rmsd`` attribute.

The algorithm used by ``Superimposer`` comes from
:raw-latex:`\cite[Golub \& Van Loan]{golub1989}` and makes use of
singular value decomposition (this is implemented in the general
``Bio.SVDSuperimposer`` module).

Example:

::

    >>> sup = Superimposer()
    # Specify the atom lists
    # 'fixed' and 'moving' are lists of Atom objects
    # The moving atoms will be put on the fixed atoms
    >>> sup.set_atoms(fixed, moving)
    # Print rotation/translation/rmsd
    >>> print(sup.rotran)
    >>> print(sup.rms)
    # Apply rotation/translation to the moving atoms
    >>> sup.apply(moving)

To superimpose two structures based on their active sites, use the
active site atoms to calculate the rotation/translation matrices (as
above), and apply these to the whole molecule.

Mapping the residues of two related structures onto each other
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, create an alignment file in FASTA format, then use the
``StructureAlignment`` class. This class can also be used for alignments
with more than two structures.

Calculating the Half Sphere Exposure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Half Sphere Exposure (HSE) is a new, 2D measure of solvent exposure
:raw-latex:`\cite{hamelryck2005}`. Basically, it counts the number of
C\ :math:`\alpha` atoms around a residue in the direction of its side
chain, and in the opposite direction (within a radius of
:math:`13 \AA`). Despite its simplicity, it outperforms many other
measures of solvent exposure.

HSE comes in two flavors: HSE\ :math:`\alpha` and HSE\ :math:`\beta`.
The former only uses the C\ :math:`\alpha` atom positions, while the
latter uses the C\ :math:`\alpha` and C\ :math:`\beta` atom positions.
The HSE measure is calculated by the ``HSExposure`` class, which can
also calculate the contact number. The latter class has methods which
return dictionaries that map a ``Residue`` object to its corresponding
HSE\ :math:`\alpha`, HSE\ :math:`\beta` and contact number values.

Example:

::

    >>> model = structure[0]
    >>> hse = HSExposure()
    # Calculate HSEalpha
    >>> exp_ca = hse.calc_hs_exposure(model, option='CA3')
    # Calculate HSEbeta
    >>> exp_cb=hse.calc_hs_exposure(model, option='CB')
    # Calculate classical coordination number
    >>> exp_fs = hse.calc_fs_exposure(model)
    # Print HSEalpha for a residue
    >>> print(exp_ca[some_residue])

Determining the secondary structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this functionality, you need to install DSSP (and obtain a license
for it — free for academic use, see http://www.cmbi.kun.nl/gv/dssp/).
Then use the ``DSSP`` class, which maps ``Residue`` objects to their
secondary structure (and accessible surface area). The DSSP codes are
listed in Table `[cap:DSSP-codes] <#cap:DSSP-codes>`__. Note that DSSP
(the program, and thus by consequence the class) cannot handle multiple
models!

.. table:: [cap:DSSP-codes]DSSP codes in Bio.PDB.

   +------+---------------------------------------+
   | Code | Secondary structure                   |
   +======+=======================================+
   | H    | :math:`\alpha`-helix                  |
   +------+---------------------------------------+
   | B    | Isolated :math:`\beta`-bridge residue |
   +------+---------------------------------------+
   | E    | Strand                                |
   +------+---------------------------------------+
   | G    | 3-10 helix                            |
   +------+---------------------------------------+
   | I    | :math:`\Pi`-helix                     |
   +------+---------------------------------------+
   | T    | Turn                                  |
   +------+---------------------------------------+
   | S    | Bend                                  |
   +------+---------------------------------------+
   | -    | Other                                 |
   +------+---------------------------------------+

The ``DSSP`` class can also be used to calculate the accessible surface
area of a residue. But see also section
`[subsec:residue_depth] <#subsec:residue_depth>`__.

Calculating the residue depth[subsec:residue_depth]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Residue depth is the average distance of a residue’s atoms from the
solvent accessible surface. It’s a fairly new and very powerful
parameterization of solvent accessibility. For this functionality, you
need to install Michel Sanner’s MSMS program
(http://www.scripps.edu/pub/olson-web/people/sanner/html/msms_home.html).
Then use the ``ResidueDepth`` class. This class behaves as a dictionary
which maps ``Residue`` objects to corresponding (residue depth,
C\ :math:`\alpha` depth) tuples. The C\ :math:`\alpha` depth is the
distance of a residue’s C\ :math:`\alpha` atom to the solvent accessible
surface.

Example:

::

    >>> model = structure[0]
    >>> rd = ResidueDepth(model, pdb_file)
    >>> residue_depth, ca_depth=rd[some_residue]

You can also get access to the molecular surface itself (via the
``get_surface`` function), in the form of a Numeric Python array with
the surface points.

Common problems in PDB files
----------------------------

It is well known that many PDB files contain semantic errors (not the
structures themselves, but their representation in PDB files). Bio.PDB
tries to handle this in two ways. The PDBParser object can behave in two
ways: a restrictive way and a permissive way, which is the default.

Example:

::

    # Permissive parser
    >>> parser = PDBParser(PERMISSIVE=1)
    >>> parser = PDBParser() # The same (default)
    # Strict parser
    >>> strict_parser = PDBParser(PERMISSIVE=0)

In the permissive state (DEFAULT), PDB files that obviously contain
errors are “corrected” (i.e. some residues or atoms are left out). These
errors include:

-  Multiple residues with the same identifier

-  Multiple atoms with the same identifier (taking into account the
   altloc identifier)

These errors indicate real problems in the PDB file (for details see
:raw-latex:`\cite[Hamelryck and Manderick, 2003]{hamelryck2003a}`). In
the restrictive state, PDB files with errors cause an exception to
occur. This is useful to find errors in PDB files.

Some errors however are automatically corrected. Normally each
disordered atom should have a non-blank altloc identifier. However,
there are many structures that do not follow this convention, and have a
blank and a non-blank identifier for two disordered positions of the
same atom. This is automatically interpreted in the right way.

Sometimes a structure contains a list of residues belonging to chain A,
followed by residues belonging to chain B, and again followed by
residues belonging to chain A, i.e. the chains are ’broken’. This is
also correctly interpreted.

Examples[problem structures]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The PDBParser/Structure class was tested on about 800 structures (each
belonging to a unique SCOP superfamily). This takes about 20 minutes, or
on average 1.5 seconds per structure. Parsing the structure of the large
ribosomal subunit (1FKK), which contains about 64000 atoms, takes 10
seconds on a 1000 MHz PC.

Three exceptions were generated in cases where an unambiguous data
structure could not be built. In all three cases, the likely cause is an
error in the PDB file that should be corrected. Generating an exception
in these cases is much better than running the chance of incorrectly
describing the structure in a data structure.

Duplicate residues
^^^^^^^^^^^^^^^^^^

One structure contains two amino acid residues in one chain with the
same sequence identifier (resseq 3) and icode. Upon inspection it was
found that this chain contains the residues Thr A3, …, Gly A202, Leu A3,
Glu A204. Clearly, Leu A3 should be Leu A203. A couple of similar
situations exist for structure 1FFK (which e.g. contains Gly B64, Met
B65, Glu B65, Thr B67, i.e. residue Glu B65 should be Glu B66).

Duplicate atoms
^^^^^^^^^^^^^^^

Structure 1EJG contains a Ser/Pro point mutation in chain A at position
22. In turn, Ser 22 contains some disordered atoms. As expected, all
atoms belonging to Ser 22 have a non-blank altloc specifier (B or C).
All atoms of Pro 22 have altloc A, except the N atom which has a blank
altloc. This generates an exception, because all atoms belonging to two
residues at a point mutation should have non-blank altloc. It turns out
that this atom is probably shared by Ser and Pro 22, as Ser 22 misses
the N atom. Again, this points to a problem in the file: the N atom
should be present in both the Ser and the Pro residue, in both cases
associated with a suitable altloc identifier.

Automatic correction
~~~~~~~~~~~~~~~~~~~~

Some errors are quite common and can be easily corrected without much
risk of making a wrong interpretation. These cases are listed below.

A blank altloc for a disordered atom
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Normally each disordered atom should have a non-blank altloc identifier.
However, there are many structures that do not follow this convention,
and have a blank and a non-blank identifier for two disordered positions
of the same atom. This is automatically interpreted in the right way.

Broken chains
^^^^^^^^^^^^^

Sometimes a structure contains a list of residues belonging to chain A,
followed by residues belonging to chain B, and again followed by
residues belonging to chain A, i.e. the chains are “broken”. This is
correctly interpreted.

Fatal errors
~~~~~~~~~~~~

Sometimes a PDB file cannot be unambiguously interpreted. Rather than
guessing and risking a mistake, an exception is generated, and the user
is expected to correct the PDB file. These cases are listed below.

.. duplicate-residues-1:

Duplicate residues
^^^^^^^^^^^^^^^^^^

All residues in a chain should have a unique id. This id is generated
based on:

-  The sequence identifier (resseq).

-  The insertion code (icode).

-  The hetfield string (“W” for waters and “H\_” followed by the residue
   name for other hetero residues)

-  The residue names of the residues in the case of point mutations (to
   store the Residue objects in a DisorderedResidue object).

If this does not lead to a unique id something is quite likely wrong,
and an exception is generated.

.. duplicate-atoms-1:

Duplicate atoms
^^^^^^^^^^^^^^^

All atoms in a residue should have a unique id. This id is generated
based on:

-  The atom name (without spaces, or with spaces if a problem arises).

-  The altloc specifier.

If this does not lead to a unique id something is quite likely wrong,
and an exception is generated.

Accessing the Protein Data Bank
-------------------------------

Downloading structures from the Protein Data Bank
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Structures can be downloaded from the PDB (Protein Data Bank) by using
the ``retrieve_pdb_file`` method on a ``PDBList`` object. The argument
for this method is the PDB identifier of the structure.

::

    >>> pdbl = PDBList()
    >>> pdbl.retrieve_pdb_file('1FAT')

The ``PDBList`` class can also be used as a command-line tool:

::

    python PDBList.py 1fat

The downloaded file will be called ``pdb1fat.ent`` and stored in the
current working directory. Note that the ``retrieve_pdb_file`` method
also has an optional argument ``pdir`` that specifies a specific
directory in which to store the downloaded PDB files.

The ``retrieve_pdb_file`` method also has some options to specify the
compression format used for the download, and the program used for local
decompression (default ``.Z`` format and ``gunzip``). In addition, the
PDB ftp site can be specified upon creation of the ``PDBList`` object.
By default, the server of the Worldwide Protein Data Bank
(ftp://ftp.wwpdb.org/pub/pdb/data/structures/divided/pdb/) is used. See
the API documentation for more details. Thanks again to Kristian Rother
for donating this module.

Downloading the entire PDB
~~~~~~~~~~~~~~~~~~~~~~~~~~

The following commands will store all PDB files in the ``/data/pdb``
directory:

::

    python PDBList.py all /data/pdb

    python PDBList.py all /data/pdb -d

The API method for this is called ``download_entire_pdb``. Adding the
``-d`` option will store all files in the same directory. Otherwise,
they are sorted into PDB-style subdirectories according to their PDB
ID’s. Depending on the traffic, a complete download will take 2-4 days.

Keeping a local copy of the PDB up to date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This can also be done using the ``PDBList`` object. One simply creates a
``PDBList`` object (specifying the directory where the local copy of the
PDB is present) and calls the ``update_pdb`` method:

::

    >>> pl = PDBList(pdb='/data/pdb')
    >>> pl.update_pdb()

One can of course make a weekly ``cronjob`` out of this to keep the
local copy automatically up-to-date. The PDB ftp site can also be
specified (see API documentation).

``PDBList`` has some additional methods that can be of use. The
``get_all_obsolete`` method can be used to get a list of all obsolete
PDB entries. The ``changed_this_week`` method can be used to obtain the
entries that were added, modified or obsoleted during the current week.
For more info on the possibilities of ``PDBList``, see the API
documentation.

General questions
-----------------

How well tested is Bio.PDB?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pretty well, actually. Bio.PDB has been extensively tested on nearly
5500 structures from the PDB - all structures seemed to be parsed
correctly. More details can be found in the Bio.PDB Bioinformatics
article. Bio.PDB has been used/is being used in many research projects
as a reliable tool. In fact, I’m using Bio.PDB almost daily for research
purposes and continue working on improving it and adding new features.

How fast is it?
~~~~~~~~~~~~~~~

The ``PDBParser`` performance was tested on about 800 structures (each
belonging to a unique SCOP superfamily). This takes about 20 minutes, or
on average 1.5 seconds per structure. Parsing the structure of the large
ribosomal subunit (1FKK), which contains about 64000 atoms, takes 10
seconds on a 1000 MHz PC. In short: it’s more than fast enough for many
applications.

Is there support for molecular graphics?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not directly, mostly since there are quite a few Python based/Python
aware solutions already, that can potentially be used with Bio.PDB. My
choice is Pymol, BTW (I’ve used this successfully with Bio.PDB, and
there will probably be specific PyMol modules in Bio.PDB soon/some day).
Python based/aware molecular graphics solutions include:

-  PyMol: http://pymol.sourceforge.net/

-  Chimera: http://www.cgl.ucsf.edu/chimera/

-  PMV: http://www.scripps.edu/~sanner/python/

-  Coot: http://www.ysbl.york.ac.uk/~emsley/coot/

-  CCP4mg: http://www.ysbl.york.ac.uk/~lizp/molgraphics.html

-  mmLib: http://pymmlib.sourceforge.net/

-  VMD: http://www.ks.uiuc.edu/Research/vmd/

-  MMTK: http://starship.python.net/crew/hinsen/MMTK/

Who’s using Bio.PDB?
~~~~~~~~~~~~~~~~~~~~

Bio.PDB was used in the construction of DISEMBL, a web server that
predicts disordered regions in proteins (http://dis.embl.de/), and
COLUMBA, a website that provides annotated protein structures
(http://www.columba-db.de/). Bio.PDB has also been used to perform a
large scale search for active sites similarities between protein
structures in the PDB
:raw-latex:`\cite[Hamelryck, 2003]{hamelryck2003b}`, and to develop a
new algorithm that identifies linear secondary structure elements
:raw-latex:`\cite[Majumdar \textit{et al.}, 2005]{majumdar2005}`.

Judging from requests for features and information, Bio.PDB is also used
by several LPCs (Large Pharmaceutical Companies :-).
