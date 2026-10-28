// ÉCHANTILLON SEULEMENT — pas un seuil de circulation.
// Généré depuis parametres.json (cm). Ici les longueurs sont en mm.
// Repère local : x vers cellier/est, y vers T1/nord, z vers le haut.
largeur = 120.0; longueur = 40.0; hauteur = 8.0; bord = 0.8;
canal = 72.0; jeu_rail = 1.0; diametre_vis = 18.0; plafond_vis = 4.0;
centre_vis_x = 58.0; centre_vis_y = 20.0;
sur_tranche = true;
$fn = 96;
module echantillon() {
  difference() {
    translate([0,longueur,0]) rotate([90,0,0])
      linear_extrude(height=longueur)
        polygon([[0,0],[largeur,0],[largeur,bord],
                 [(largeur+canal)/2,hauteur],[(largeur-canal)/2,hauteur],[0,bord]]);
    translate([(largeur-canal)/2,-1,-1]) cube([canal,longueur+2,jeu_rail+1]);
    translate([centre_vis_x,centre_vis_y,-1]) cylinder(h=plafond_vis+1,d=diametre_vis);
  }
}
if (sur_tranche) translate([0,0,longueur]) rotate([-90,0,0]) echantillon();
else echantillon();
