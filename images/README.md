# /images — drop your real photos here

When the build is done, export photos (landscape, min 2000px wide, bright)
and save them in this folder with these names, then swap the placeholder
blocks in index.html.

Files to add:
  hero.jpg        -> the wide living/balcony hero shot (used in og:image too)
  living.jpg      -> about section (replace .ph.ph-living)
  bedroom.jpg     -> gallery (replace .ph.ph-bed)
  bathroom.jpg    -> gallery (replace .ph.ph-bath)
  balcony.jpg     -> gallery (replace .ph.ph-balcony)
  skylight.jpg    -> gallery (replace .ph.ph-skylight)
  map.jpg         -> location section (replace .ph.ph-map)  OR keep the CSS map

How to swap (example for the about section):
  Replace:
    <div class="ph ph-living"><span class="ph-tag">Living & balcony · add photo</span></div>
  With:
    <img class="ph" src="images/living.jpg" alt="Bright living room with balcony and hill view" />

The .ph class already gives it the right aspect ratio, radius and shadow.
