<table border='1' cellspacing='0'>
<tr>
<td>
<h3>Update 13-Jun-2014: 1.1.15-beta</h3>
<ul><li>WebP support<br>
</li><li>Added user-configurable API key for Comic Vine access<br>
</li><li>Experimental option to wait and retry after exceeding Comic Vine rate limit</li></ul>


(Visit <a href='ReleaseNotes.md'>Release Notes</a> for more history.)<br>
</td>
</tr>
</table>

<table border='1' cellspacing='0'>
<tr>
<td>

<h3>Announcement</h3>
Comic Vine has made changes that limit the amount of requests that can<br>
be made for each API key.  By default, ComicTagger uses the same<br>
key for all installations, which often exhausts the limit.<br>
<br>
Each user should register an account with Comic Vine to get his or her own API key.<br>
ComicTagger now allows the user to configure their personal key for searching.<br>
Please visit <a href='http://www.comicvine.com/api/'>Comic Vine</a> to register, and get your key.<br>
<br>
Visit the <a href='UserGuide#Comic_Vine.md'>wiki</a> for more info.<br>
</td>
</tr>
</table>


&lt;wiki:gadget url="https://comictagger.googlecode.com/svn/trunk/google/gadgets/social.xml" height="70" width="600" border="0" /&gt;<br />
<img src='https://lh3.googleusercontent.com/-ZjqcxDiXZvE/UQCDHvX84jI/AAAAAAAAAE4/11Jjp2NnDCI/s1152/mac1.png' width='600'>


<b><a href='Home.md'>ComicTagger</a></b> is a multi-platform app for writing metadata to digital comic archives, written in Python and PyQt.<br>
<br>
Features:<br>
<br>
<ul><li>Runs on Mac OSX, Microsoft Windows, and Linux systems<br>
</li><li>Communicates with an online database (Comic Vine) for acquiring metadata<br>
</li><li>Uses image processing to automatically match a given archive with the correct issue data<br>
</li><li>Batch processing in the GUI for tagging hundreds or more comics at a time<br>
</li><li>Reads and writes multiple tagging schemes ( ComicBookLover and ComicRack, with more planned).<br>
</li><li>Reads and writes RAR and Zip (CBR and CBZ) archives (external tools needed for writing RAR)<br>
</li><li>Rename files based on tag info<br>
</li><li>Convert CBR/RAR files to CBZ/ZIP format<br>
</li><li>Command line interface (CLI) on all platforms (including Windows), which supports batch operations, and which can be used in native scripts for complex operations.  For example, to recursively tag all archives in a folder:<br>
<blockquote><code>ComicTagger -R -s -o -f -t cr /path/to/comics/</code></blockquote></li></ul>

For details, screenshots, release notes, and more,  visit the <a href='Home.md'>wiki</a>!<br>
<br>
<br>
If you have any comments, questions, feature requests, and issues post here:<br>
<ul><li>The <a href='http://code.google.com/p/comictagger/issues/list'>Issues</a> tab on this site<br>
</li><li>The forum here: <a href='http://comictagger.forumotion.com/'>http://comictagger.forumotion.com/</a></li></ul>

<h2>Donations and Adorations</h2>

If you like ComicTagger, and want to express it, make a donation to buy me a beer or a coffee!<br>
<ul><li><b>Paypal:</b> <a href='https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=comictagger%40gmail%2ecom&lc=US&item_name=ComicTagger%20Project&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted'><img src='https://www.paypal.com/en_US/i/btn/btn_donate_LG.gif' /></a></li></ul>


Or, if you just want to spread the good word, rate ComicTagger, or write a review, at the some of the following sites:<br>
<br>
<ul><li><b><a href='http://www.macupdate.com/app/mac/47099/comictagger'>MacUpdate</a></b>
</li><li><b><a href='http://www.softpedia.com/get/Multimedia/Graphic/Graphic-Others/ComicTagger.shtml'>Softpedia (Windows)</a></b>
</li><li><b><a href='http://mac.softpedia.com/get/Utilities/ComicTagger.shtml'>Softpedia (Mac)</a></b>
</li><li><b><a href='http://linux.softpedia.com/get/Multimedia/Graphics/ComicTagger-96265.shtml'>Softpedia (Linux)</a></b>
</li><li><b><a href='http://download.cnet.com/ComicTagger/3000-2130_4-75827445.html'>CNET (Windows)</a></b>