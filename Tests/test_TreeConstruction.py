# Copyright (C) 2013 by Yanbo Ye (yeyanbo289@gmail.com)
# This code is part of the Biopython distribution and governed by its
# license. Please see the LICENSE file that should have been included
# as part of this package.

"""Unit tests for the Bio.TreeConstruction module."""

import logging
import unittest
from Bio import AlignIO
from Bio import Phylo
from Bio.Phylo import BaseTree
from Bio.Phylo import TreeConstruction
from Bio.Phylo.TreeConstruction import Matrix
from Bio.Phylo.TreeConstruction import DistanceMatrix
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import ParsimonyScorer
from Bio.Phylo.TreeConstruction import NNITreeSearcher

logging.basicConfig(filename='./TreeConstruction/test.log', level=logging.DEBUG)

class DistanceMatrixTest(unittest.TestCase):
    """Test for DistanceMatrix construction and manipulation"""

    def test_good_construction(self):
        names = ['Alpha', 'Beta', 'Gamma', 'Delta']
        matrix = [[0], [1, 0], [2, 3, 0], [4, 5, 6, 0]]
        dm = DistanceMatrix(names, matrix)
        self.assertTrue(isinstance(dm, TreeConstruction.DistanceMatrix))
        self.assertEqual(dm.names[0], 'Alpha')
        self.assertEqual(dm.matrix[2][1], 3)
        self.assertEqual(len(dm), 4)

    def test_bad_construction(self):
        self.assertRaises(TypeError, DistanceMatrix, ['Alpha', 100, 'Gamma', 'Delta'], [[0], [0.1, 0], [0.2, 0.3, 0], [0.4, 0.5, 0.6, 0]])
        self.assertRaises(TypeError, DistanceMatrix, ['Alpha', 'Beta', 'Gamma', 'Delta'], [[0], ['a'], [0.2, 0.3], [0.4, 0.5, 0.6]])
        self.assertRaises(ValueError, DistanceMatrix, ['Alpha', 'Alpha', 'Gamma', 'Delta'], [[0], [0.1], [0.2, 0.3], [0.4, 0.5, 0.6]])
        self.assertRaises(ValueError, DistanceMatrix, ['Alpha', 'Beta', 'Gamma', 'Delta'], [[0], [0.2, 0], [0.4, 0.5, 0.6]])
        self.assertRaises(ValueError, DistanceMatrix, ['Alpha', 'Beta', 'Gamma', 'Delta'], [[0], [0.1], [0.2, 0.3, 0.4], [0.4, 0.5, 0.6]])

    def test_good_manipulation(self):
        names = ['Alpha', 'Beta', 'Gamma', 'Delta']
        matrix = [[0], [1, 0], [2, 3, 0], [4, 5, 6, 0]]
        dm = DistanceMatrix(names, matrix)
        # getitem
        self.assertEqual(dm[1], [1, 0, 3, 5])
        self.assertEqual(dm[2, 1], 3)
        self.assertEqual(dm[2][1], 3)
        self.assertEqual(dm[1, 2], 3)
        self.assertEqual(dm[1][2], 3)
        self.assertEqual(dm['Alpha'], [0, 1, 2, 4])
        self.assertEqual(dm['Gamma', 'Delta'], 6)
        # setitem
        dm['Alpha'] = [0, 10, 20, 40]
        self.assertEqual(dm['Alpha'], [0, 10, 20, 40])
        # delitem insert item
        del dm[1]
        self.assertEqual(dm.names, ['Alpha', 'Gamma', 'Delta'])
        self.assertEqual(dm.matrix, [[0], [20, 0], [40, 6, 0]])
        dm.insert('Beta', [1, 0, 3, 5], 1)
        self.assertEqual(dm.names, names)
        self.assertEqual(dm.matrix, [[0], [1, 0], [20, 3, 0], [40, 5, 6, 0]])
        del dm['Alpha']
        self.assertEqual(dm.names, ['Beta', 'Gamma', 'Delta'])
        self.assertEqual(dm.matrix, [[0], [3, 0], [5, 6, 0]])
        dm.insert('Alpha', [1, 2, 4, 0])
        self.assertEqual(dm.names, ['Beta', 'Gamma', 'Delta', 'Alpha'])
        self.assertEqual(dm.matrix, [[0], [3, 0], [5, 6, 0], [1, 2, 4, 0]])

    def test_bad_manipulation(self):
        names = ['Alpha', 'Beta', 'Gamma', 'Delta']
        matrix = [[0], [1, 0], [2, 3, 0], [4, 5, 6, 0]]
        dm = DistanceMatrix(names, matrix)
        #getitem
        self.assertRaises(ValueError, dm.__getitem__, 'A')
        self.assertRaises(ValueError, dm.__getitem__, ('Alpha', 'A'))
        self.assertRaises(TypeError, dm.__getitem__, (1, 'A'))
        self.assertRaises(TypeError, dm.__getitem__, (1, 1.2))
        self.assertRaises(IndexError, dm.__getitem__, 6)
        self.assertRaises(IndexError, dm.__getitem__, (10, 10))
        #setitem: item or index test
        self.assertRaises(ValueError, dm.__setitem__, 'A', [1, 3, 4])
        self.assertRaises(ValueError, dm.__setitem__, ('Alpha', 'A'), 4)
        self.assertRaises(TypeError, dm.__setitem__, (1, 'A'), 3)
        self.assertRaises(TypeError, dm.__setitem__, (1, 1.2), 2)
        self.assertRaises(IndexError, dm.__setitem__, 6, [1, 3, 4])
        self.assertRaises(IndexError, dm.__setitem__, (10, 10), 1)
        #setitem: value test
        self.assertRaises(ValueError, dm.__setitem__, 0, [1, 2])
        self.assertRaises(TypeError, dm.__setitem__, ('Alpha', 'Beta'), 'a')
        self.assertRaises(TypeError, dm.__setitem__, 'Alpha', ['a', 'b', 'c'])

class DistanceCalculatorTest(unittest.TestCase):
    """Test DistanceCalculator"""

    def test_distance_calculator(self):
        aln = AlignIO.read(open('TreeConstruction/msa.phy'), 'phylip')

        calculator = DistanceCalculator(aln, 'identity')
        dm = calculator.get_distance()
        self.assertEqual(dm['Alpha', 'Beta'], 1 - (10 * 1.0 / 13))

        calculator = DistanceCalculator(aln, 'blastn')
        dm = calculator.get_distance()
        self.assertEqual(dm['Alpha', 'Beta'], 1 - (38 * 1.0 / 65))

        calculator = DistanceCalculator(aln, 'trans')
        dm = calculator.get_distance()
        self.assertEqual(dm['Alpha', 'Beta'], 1 - (49 * 1.0 / 78))

        calculator = DistanceCalculator(aln, 'blosum62')
        dm = calculator.get_distance()
        self.assertEqual(dm['Alpha', 'Beta'], 1 - (53 * 1.0 / 84))


class DistanceTreeConstructorTest(unittest.TestCase):
    """Test DistanceTreeConstructor"""

    def test_upgma(self):
        aln = AlignIO.read(open('TreeConstruction/msa.phy'), 'phylip')

        calculator = DistanceCalculator(aln, 'blosum62')
        dm = calculator.get_distance()
        logging.info("DistanceMatrix:\n" + str(dm))
        constructor = DistanceTreeConstructor(dm)
        tree = constructor.upgma()
        self.assertTrue(isinstance(tree, BaseTree.Tree))
        logging.info("UPGMA Tree:\n" + str(tree))
        Phylo.write(tree, './TreeConstruction/upgma.tre', 'newick')

    def test_nj(self):
        aln = AlignIO.read(open('TreeConstruction/msa.phy'), 'phylip')

        calculator = DistanceCalculator(aln, 'blosum62')
        dm = calculator.get_distance()
        logging.info("DistanceMatrix:\n" + str(dm))
        constructor = DistanceTreeConstructor(dm)
        tree = constructor.nj()
        self.assertTrue(isinstance(tree, BaseTree.Tree))
        logging.info("NJ Tree:\n" + str(tree))
        Phylo.write(tree, './TreeConstruction/nj.tre', 'newick')

class ParsimonyScorerTest(unittest.TestCase):
    """Test ParsimonyScorer"""

    def test_get_score(self):
        aln = AlignIO.read(open('TreeConstruction/msa.phy'), 'phylip')
        tree = Phylo.read('./TreeConstruction/upgma.tre', 'newick')
        scorer = ParsimonyScorer()
        score = scorer.get_score(tree, aln)
        self.assertEqual(score, 2 + 1 + 2 + 2 + 1 + 1 + 1 + 3)

        alphabet = ['A', 'T', 'C', 'G']
        step_matrix = [[0],
                       [2.5,   0],
                       [2.5,   1,    0],
                       [  1, 2.5,  2.5, 0]]
        matrix = Matrix(alphabet, step_matrix)
        scorer = ParsimonyScorer(matrix)
        score = scorer.get_score(tree, aln)
        self.assertEqual(score, 3.5 + 2.5 + 3.5 + 3.5 + 2.5 + 1 + 2.5 + 4.5)

        alphabet = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', '1', '2', 'T', 'V', 'W', 'Y', '*', '-']
        step_matrix = [[0],
                       [2, 0],
                       [1, 2, 0],
                       [1, 2, 1, 0],
                       [2, 1, 2, 2, 0],
                       [1, 1, 1, 1, 2, 0],
                       [2, 2, 1, 2, 2, 2, 0],
                       [2, 2, 2, 2, 1, 2, 2, 0],
                       [2, 2, 2, 1, 2, 2, 2, 1, 0],
                       [2, 2, 2, 2, 1, 2, 1, 1, 2, 0],
                       [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0],
                       [2, 2, 1, 2, 2, 2, 1, 1, 1, 2, 2, 0],
                       [1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0],
                       [2, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 0],
                       [2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0],
                       [1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0],
                       [2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 0],
                       [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 0],
                       [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0],
                       [2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 3, 2, 2, 1, 1, 2, 2, 2, 0],
                       [2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 3, 1, 2, 2, 2, 1, 2, 2, 2, 2, 0],
                       [2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 0],
                       [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0]]

        matrix = Matrix(alphabet, step_matrix)
        scorer = ParsimonyScorer(matrix)
        score = scorer.get_score(tree, aln)
        self.assertEqual(score, 3 + 1 + 3 + 3 + 2 + 1 + 2 + 5)


class NNITreeSearcherTest(unittest.TestCase):
    """Test NNITreeSearcher"""

    def test_get_neighbors(self):
        tree = Phylo.read('./TreeConstruction/upgma.tre', 'newick')
        alphabet = ['A', 'T', 'C', 'G']
        step_matrix = [[0],
                       [2.5,   0],
                       [2.5,   1,    0],
                       [  1, 2.5,  2.5, 0]]
        matrix = Matrix(alphabet, step_matrix)
        scorer = ParsimonyScorer(matrix)
        searcher = NNITreeSearcher(scorer)
        trees = searcher._get_neighbors(tree)
        self.assertEqual(len(trees), 2 * (5 - 3))
        Phylo.write(trees, './TreeConstruction/neighbor_trees.tre', 'newick')

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)