from itertools import product
from typing import List

from pydefect.input_maker.complex_defect2 import ComplexDefect2
from pydefect.input_maker.complex_defect2_set import ComplexDefect2Set
from pydefect.input_maker.defect import SimpleDefect
from pydefect.input_maker.defect_set import DefectSet
from pydefect.input_maker.defect_set import DefectSet


class ComplexDefect2SetMaker:
    """
    A class to generate a set of ComplexDefect2 objects based on a given DefectSet and
    a set of candidate ComplexDefect2 definitions.

    Attributes:
        defect_set (DefectSet): The set of simple defects to consider.
        candidate_complex_defect2_set (ComplexDefect2Set): The set of candidate complex defects.
        complex_defect2_set (ComplexDefect2Set): The generated set of ComplexDefect2 objects.
    """

    def __init__(
        self,
        defect_set: DefectSet,
        candidate_complex_defect2_set: ComplexDefect2Set
    ) -> None:
        """
        Initializes the ComplexDefect2SetMaker with a DefectSet and a set of candidate ComplexDefect2.

        Args:
            defect_set (DefectSet): The set of simple defects to consider.
            candidate_complex_defect2_set (ComplexDefect2Set): The set of candidate complex defects.
        """
        self.defect_set = defect_set
        self.candidate_complex_defect2_set = candidate_complex_defect2_set
        self.complex_defect2_set = self._create_complex_defect2_set()

    def _create_complex_defect2_set(self) -> ComplexDefect2Set:
        """
        Generates a ComplexDefect2Set by combining candidate complex defects with possible simple defects.

        This method processes each candidate complex defect by:
            - Retrieving possible simple defects associated with each sub-defect, considering their in and out atoms.
            - Creating all possible combinations of these simple defects.
            - Sorting each combination and instantiating a ComplexDefect2 object with a unique name and corresponding charges.

        The resulting ComplexDefect2Set is sorted based on the concatenated in and out atoms of the sub-defects to ensure consistent ordering.

        Returns:
            ComplexDefect2Set: A sorted set containing all possible ComplexDefect2 instances generated from the candidates.
        """
        complex_defect2_instances = set()

        for candidate_defect in self.candidate_complex_defect2_set:
            # Prepare lists to hold possible simple defects for each sub-defect
            simple_defects_combinations: List[List[SimpleDefect]] = [
                [] for _ in candidate_defect.sub_defects
            ]
            # Populate simple_defects_combinations with matching simple defects
            for idx, sub_defect in enumerate(candidate_defect.sub_defects):
                matching_defects = self._get_matching_defects(sub_defect)
                if not matching_defects:
                    raise ValueError(f"No matching defects found for {sub_defect}.")
                simple_defects_combinations[idx].extend(matching_defects)

            # Generate all possible combinations of simple defects
            for simple_defect_combo in product(*simple_defects_combinations):
                # Sort the combination to maintain consistent ordering
                sorted_defects = sorted(
                    simple_defect_combo,
                    key=lambda defect: f"{defect.in_atom}_{defect.out_atom}"
                )

                # Generate a unique name for the complex defect
                unique_name = "complex_" + "+".join(
                    f"{sd.in_atom}_{sd.out_atom}" if sd.in_atom is not None else f"Va_{sd.out_atom}" for sd in sorted_defects
                )

                # Create a ComplexDefect2 instance
                complex_defect = ComplexDefect2(
                    sub_defects=sorted_defects,
                    name=unique_name,
                    charges=candidate_defect.charges
                )

                complex_defect2_instances.add(complex_defect)

        # Sort the ComplexDefect2 instances based on their sub-defects' in and out atoms
        sorted_complex_defects = sorted(
            complex_defect2_instances,
            key=lambda cd: "_".join(
                f"{sd.in_atom}_{sd.out_atom}" for sd in cd.sub_defects
            )
        )

        return ComplexDefect2Set(sorted_complex_defects)

    def _get_matching_defects(self, sub_defect: SimpleDefect) -> List[SimpleDefect]:
        """
        Retrieves a list of simple defects from the defect_set that match the given sub_defect's
        in_atom and the non-numeric part of out_atom.

        Args:
            sub_defect (SimpleDefect): The sub-defect to match.

        Returns:
            List[SimpleDefect]: A list of matching simple defects.
        """
        matching_defects = []
        for defect in self.defect_set.defects:
            # Extract the non-numeric part of out_atom
            non_numeric_out_atom = ''.join(filter(str.isalpha, defect.out_atom))

            if (
                non_numeric_out_atom == sub_defect.out_atom and
                defect.in_atom == sub_defect.in_atom
            ):
                matching_defects.append(defect)

        return matching_defects
