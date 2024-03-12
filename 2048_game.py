import random
import tkinter as tk
import tkinter.messagebox

class Grille:
    def __init__(self, taille):
        self.taille = taille
        self.cases = [[0] * taille for _ in range(taille)]

    def generer_grille_vide(self):
        return [[0] * self.taille for _ in range(self.taille)]

    def cellule_aleatoire(self):
        vides = [(x, y) for x in range(self.taille) for y in range(self.taille) if self.cases[x][y] == 0]
        if vides:
            x, y = random.choice(vides)
            self.cases[x][y] = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.25, 0.05])[0]

    def recuperer_cases_vides(self):
        return [(x, y) for x in range(self.taille) for y in range(self.taille) if self.cases[x][y] == 0]

class PanneauJeu:
    ESPACEMENT_CELLULE = 1
    COULEUR_FOND = '#ffffff'
    COULEUR_CELLULE_VIDE = '#9e948a'
    COULEURS_CELLULES = ['#b0c2f2', '#FFABAB', '#FFC3A0', '#FF677D', '#D4A5A5', '#392F5A', '#31A2AC', '#61C0BF', '#6B4226', '#D9BF77']
    POLICE = ('Verdana', 24, 'bold')

    def __init__(self, grille, jeu):
        self.grille = grille
        self.jeu = jeu
        self.root = tk.Tk()
        self.root.title('Just Get 10')
        self.fond = tk.Frame(self.root, bg=self.COULEUR_FOND)
        self.etiquettes_cellules = [[None for _ in range(grille.taille)] for _ in range(grille.taille)]
        self.initialiser_interface()

    def initialiser_interface(self):
        for x in range(self.grille.taille):
            for y in range(self.grille.taille):
                valeur_cellule = self.grille.cases[x][y]
                etiquette = tk.Label(self.fond, text=str(valeur_cellule) if valeur_cellule > 0 else '', bg=self.COULEUR_CELLULE_VIDE,
                                     font=self.POLICE, width=4, height=2)
                etiquette.grid(row=x, column=y, padx=self.ESPACEMENT_CELLULE, pady=self.ESPACEMENT_CELLULE)
                etiquette.bind('<Button-1>', lambda event, x=x, y=y: self.jeu.on_clic(x, y))
                self.etiquettes_cellules[x][y] = etiquette
        self.fond.pack()

    def rafraichir(self):
        for x in range(self.grille.taille):
            for y in range(self.grille.taille):
                valeur_cellule = self.grille.cases[x][y]
                self.etiquettes_cellules[x][y]['text'] = str(valeur_cellule) if valeur_cellule > 0 else ''
                self.etiquettes_cellules[x][y]['bg'] = self.COULEURS_CELLULES[valeur_cellule - 1] if valeur_cellule > 0 else self.COULEUR_CELLULE_VIDE

class Jeu:
  def __init__(self, taille):
      self.grille = Grille(taille)
      self.panneau = PanneauJeu(self.grille, self)
      self.nombre_cellules_initiales = 25

  def demarrer(self):
      for _ in range(self.nombre_cellules_initiales):
          self.grille.cellule_aleatoire()
      self.panneau.rafraichir()
      self.panneau.root.mainloop()

  def on_clic(self, x, y):
    valeur = self.grille.cases[x][y]
    if valeur == 0:
        return
  
    if self.peut_fusionner(x, y, valeur):
        self.fusionner_cellules_adjacentes(x, y, valeur)
        self.grille.cases[x][y] += 1  # Incrémenter uniquement la cellule cliquée
        self.appliquer_gravite()  # Déplacer les cellules vers le bas
        self.remplir_grille()  # Remplir les cases vides avec de nouvelles cellules
        self.grille.cellule_aleatoire()  # Optionnel, selon que vous voulez ajouter une cellule aléatoire supplémentaire après le remplissage
  
    
    self.panneau.rafraichir()

    if self.est_game_over():
        # Afficher le message de "Game Over" et la boîte de dialogue
        self.afficher_boite_dialogue_fin_jeu("Game Over")
    elif self.est_victoire():
        # Afficher le message de "Victoire" et la boîte de dialogue
        self.afficher_boite_dialogue_fin_jeu("Victoire")
      
  def est_game_over(self):
      for x in range(self.grille.taille):
        for y in range(self.grille.taille):
            valeur = self.grille.cases[x][y]
            if valeur == 0:
                return False  # Il y a encore au moins une case vide
            if self.peut_fusionner(x, y, valeur):
                return False  # Les cellules peuvent encore fusionner
        return True  # Aucun mouvement valide disponible
  
  
  def est_victoire(self):
    for x in range(self.grille.taille):
        for y in range(self.grille.taille):
            if self.grille.cases[x][y] == 10:
                return True  # La valeur 10 a été atteinte
    return False  # Aucune cellule avec la valeur 10 sur le tableau
  

  def afficher_boite_dialogue_fin_jeu(self, message):
      resultat = tkinter.messagebox.askquestion("Fin du Jeu", message + "\nVoulez-vous jouer à nouveau ?")
      if resultat == 'yes':
          # Redémarrer le jeu (commencer un nouveau jeu)
          self.recommencer_jeu()
      else:
        # Fermer le jeu
        self.panneau.root.destroy()
      
  def peut_fusionner(self, x, y, valeur):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions : haut, bas, gauche, droite
        nouvelle_x, nouvelle_y = x + dx, y + dy
        if 0 <= nouvelle_x < self.grille.taille and 0 <= nouvelle_y < self.grille.taille:  # Vérifie si la nouvelle position est dans la grille
            if self.grille.cases[nouvelle_x][nouvelle_y] == valeur:
                return True
    return False

  def fusionner_cellules_adjacentes(self, x, y, valeur):
      def fusionner(x, y):
          if 0 <= x < self.grille.taille and 0 <= y < self.grille.taille and self.grille.cases[x][y] == valeur:
              self.grille.cases[x][y] = 0  # Effacer la valeur de cette case
              for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                  fusionner(x + dx, y + dy)
      # Éviter d'effacer la valeur de la case cliquée initialement en plaçant cette ligne après l'appel récursif.
      fusionner(x, y)
      self.grille.cases[x][y] = valeur  # Rétablir la valeur de la case cliquée pour son incrémentation ultérieure dans on_clic.

  def appliquer_gravite(self):
      for col in range(self.grille.taille):
          for ligne in range(self.grille.taille - 2, -1, -1):  # Commencer à l'avant-dernière ligne et remonter
              if self.grille.cases[ligne][col] != 0 and self.grille.cases[ligne + 1][col] == 0:
                  # Déplacer les cellules vers le bas s'il y a de la place
                  ligne_courante = ligne
                  while ligne_courante < self.grille.taille - 1 and self.grille.cases[ligne_courante + 1][col] == 0:
                      self.grille.cases[ligne_courante + 1][col] = self.grille.cases[ligne_courante][col]
                      self.grille.cases[ligne_courante][col] = 0
                      ligne_courante += 1

  def remplir_grille(self):
    for col in range(self.grille.taille):
        cases_vides_dans_colonne = [ligne for ligne in range(self.grille.taille) if self.grille.cases[ligne][col] == 0]
        while cases_vides_dans_colonne:
            ligne = cases_vides_dans_colonne.pop(0)
            self.grille.cases[ligne][col] = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.25, 0.05])[0]

  def recommencer_jeu(self):
      self.grille = Grille(self.grille.taille)
      self.panneau = PanneauJeu(self.grille, self)
      self.nombre_cellules_initiales = 25
      self.demarrer()

if __name__ == '__main__':
  jeu = Jeu(5)
  jeu.demarrer()
