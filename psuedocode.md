<H1>I'm Stuck</H1>

<p>So here's the ish. I am gonna start out with some brand new psuedo code because my good ol code that's written is being 
stubborn. What's my problem? I don't know what order of operations I should be doing. Do I add truck based packages first?
Do I pair packages first and place them on whatever truck? Do I create the most efficient routes first and completely forget 
about the packages for the time being? Maybe that one, that sounds real good. Let's break down pro's and cons of some...</p>

<H2>Truck based packages first</H2>
<H3>Pro's:</H3>
<ul>
<li>No need to worry about the truck specific packages</li>
</ul>

<H3>Con's</H3>
<ul>
<li>Uhhh idk, can't brain rn</li>
</ul>

<H2>Pair packages first</H2>
<H3>Pro's:</H3>
<ul>
<li>Makes package groups up front</li>
</ul>

<H3>Con's</H3>
<ul>
<li>May create conflicts with truck and package pairings</li>
</ul>

<H2>Create routes first</H2>
<H3>Pro's:</H3>
<ul>
<li>Route efficiency done</li>
</ul>

<H3>Con's</H3>
<ul>
<li>Most efficient routes might not account for other package requirements</li>
</ul>

<H2>A combination, package requirements first (including time but that can be post probably), unassigned to trucks, then find most efficient route that has those packages</H2>
<H3>Pro's:</H3>
<ul>
<li>All package requirements accounted for</li>
<li>Routes will take requirements into account</li>
</ul>

<H3>Con's</H3>
<ul>
<li>More complex harder for brain to make</li>
</ul>

<p>So obviously, there's only one choice here that'll work. What I think it'll need is...</p>

<ol>
<li>Create lists that aren't paired to the trucks</li>
<li>Only make the same amount of initial lists as the amount of trucks</li>
<li>Look for package pairings first, then if any of those pairings have a truck requirement, add the remaining packages 
with the truck requirement to that list, if a package has a time requirement but no special note, add it to a list as well</li>
<li>For the routes:
    <ol>
    <li>Take the 3 (or the amount of trucks) farthest points on the map as the end points for the initial outbound route</li>
    <li>Make reverse routes from the end point to the hub, combine the initial and reverse routes with all possibilities 
    that don't have duplicate stops</li>
    <li>Find routes that match a current lists requirements</li>
    <li>Once a route is finalized, remove those points (minus the hub) from the graph</li>
    <li><b>!!! As this is all happening reference the existing package lists to make sure paired packages stay together and
    truck specific packages do as well AND ALSO THE GOSH DANG PACKAGES WITH TIMES ON THEM !!!</b></li>
    <li>Check the time and miles of each of those lists if it goes beyond the limit of the requirements, give up and 
    drop out of college</li>
    </ol>
</li>
<li>Based on the routes, add packages to the lists</li>
<li>If any list has a specific truck, assign those lists to the truck</li>
<li>Assign other lists to an empty truck</li>
<li>Update package status's</li>
<li>Execute the routes</li>
<li>First route done, take the late packages out</li>
<li>If the address change is done before the first truck is back, add it to the above, otherwise the next truck back takes it</li>
<li>Have a pretty little gui to show progress with a checkbox for simulation
    <ul>
    <li>Maybe prompt for truck amount and mile limit etc. Just for fun</li>
    </ul>
</li>
<li>Be done with this class</li>
</ol>