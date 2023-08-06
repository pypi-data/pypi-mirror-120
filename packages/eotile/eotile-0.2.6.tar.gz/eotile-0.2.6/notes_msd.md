pas d'option pour avoir la version

retourner un gdf sur la sortie standard
id tile id tile_type geometry(WKT)


eotile 31TCJ -> uniquement les infos S2

eotile 198030 -> uniquement les infos L8

ajouter -s2 pour sortir les infos des tuiles s2

ajouter -l8 pour sortir les infos des tuiles L8

ajouter -dem pour sortir les infos des tuiles ( préciser pour dem3s ?)

si -location on ajoute dans le gdf la localisation dy centroid de la tuile (city, country)

si input = tile_id
 on sort les infos que type de tuile identifié

si input = autre type l'utilisateur doit fournir quel type de tuile il veut en sortie