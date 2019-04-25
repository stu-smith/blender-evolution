from .genome_expression import GenomeExpression
from .lighting.lighting_gene_property import LightingGeneProperty
from .hierarchy.hierarchical_gene_property import HierarchicalGeneProperty


class Genome(object):

    def __init__(self):
        self._hierarchical_gene_property = HierarchicalGeneProperty()
        self._lighting_gene_property = LightingGeneProperty()

    def mutate(self, configuration):
        self._hierarchical_gene_property.mutate(configuration)
        self._lighting_gene_property.mutate(configuration)

    def express(self):
        genome_expression = GenomeExpression()
        self._hierarchical_gene_property.gene.express(genome_expression)
        self._lighting_gene_property.gene.express(genome_expression)
        return genome_expression
