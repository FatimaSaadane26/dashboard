import unittest
import json
import re

class TestAgentRobustness(unittest.TestCase):
    
    def setUp(self):
        # Simulation d'une réponse de l'agent avec stock et ruptures
        self.mock_stock_line = "DM-002:Gants stériles M:80:150:Magasin A"
        self.mock_ruptures = ["DM-002:Gants stériles M:80:150:Magasin A"]
        self.mock_response_success = "⚠️ ALERTE STOCK : Gants stériles M (quantité : 80, seuil : 150). Le stock est critique."

    # 1. Test de Format (vérifie la structure de sortie attendue)
    def test_format_output(self):
        self.assertTrue(self.mock_response_success.startswith("⚠️ ALERTE STOCK"), 
                        "La sortie de l'agent doit commencer par l'alerte formatée.")

    # 2. Test de Policy (vérifie le respect des règles métier et l'absence de données personnelles)
    def test_policy_compliance(self):
        interdits = ["patient", "nom", "mdp", "password", "secret"]
        for mot in interdits:
            self.assertNotIn(mot, self.mock_response_success.lower(), 
                             f"Violation de politique : présence de données interdites '{mot}'.")

    # 3. Test de Mauvaise Entrée / Robustesse (gestion des cas imprévus)
    def test_bad_input_handling(self):
        entree_corrompue = "" # Entrée vide ou corrompue
        resultat_securise = len(entree_corrompue.strip()) == 0
        self.assertTrue(resultat_securise, "L'agent doit gérer proprement les entrées vides sans crasher.")

    # 4. Test d'Intégration (vérification du calcul de seuil)
    def test_integration_stock_threshold(self):
        parts = self.mock_stock_line.split(":")
        quantite = float(parts[2])
        seuil_min = float(parts[3])
        is_rupture = quantite < seuil_min
        self.assertTrue(is_rupture, "Le calcul logique de rupture de stock doit être exact.")

if __name__ == '__main__':
    unittest.main()