# QuickHTML

A simple Markdown to HTML preprocessor that doesn't require any third-party modules.

Quickly generate HTML from Markdown, using python.

## Technologies used

- Python
- RegEx

# Installation

QuickHTML is a Python module, if Python is not already installed in your system, you can get the latest version [here](https://python.org/downloads/) or using a package manager. pip should be installed with Python by default, if not, you can get it [here](https://pip.pypa.io/en/stable/installing/).

QuickHTML can then be installed using pip, by running `pip install quickhtml` on the command line.

# Usage

To see how to use QuickHTML directly from the terminal, run `python -m quickhtml -h`.

To import QuickHTML in Python files, use:

```
>>> import quickhtml
>>> ...
```

The `convert()` function accepts a string, and returns it formatted as HTML:

```
>>> string = "# This is a level 1 heading."
>>> quickhtml.convert(string)
'<h1>This is a level 1 heading.</h1>'
>>> ...
```

The `convert_file()` function accepts a file path, and returns the file content formatted as HTML:

```
>>> file_path = "./markdown_documents/example_document.md"
>>> quickhtml.convert_file(file_path)
'<p>This is an example document.</p>'
>>> ...
```

# Supported syntax

## Headings

To create a heading, add a number of pound (`#`) signs before a word or phrase. The number of signs corresponds to the heading level, up to six levels. For example, to create a level three heading (`<h3>`), use three pound signs (`### This is a level three heading.`).

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code># This is a level 1 heading.</code></td>
            <td><code>&lt;h1&gt;This is a level 1 heading.&lt;/h1&gt;</code></td>
            <td><h1>This is a level 1 heading.</h1></td>
        </tr>
            <tr>
            <td><code>## This is a level 2 heading.</code></td>
            <td><code>&lt;h2&gt;This is a level 2 heading.&lt;/h2&gt;</code></td>
            <td><h2>This is a level 2 heading.</h2></td>
        </tr>
            <tr>
            <td><code>### This is a level 3 heading.</code></td>
            <td><code>&lt;h3&gt;This is a level 3 heading.&lt;/h3&gt;</code></td>
            <td><h3>This is a level 3 heading.</h3></td>
        </tr>
            <tr>
            <td><code>#### This is a level 4 heading.</code></td>
            <td><code>&lt;h4&gt;This is a level 4 heading.&lt;/h4&gt;</code></td>
            <td><h4>This is a level 4 heading.</h4></td>
        </tr>
            <tr>
            <td><code>##### This is a level 5 heading.</code></td>
            <td><code>&lt;h5&gt;This is a level 5 heading.&lt;/h5&gt;</code></td>
            <td><h5>This is a level 5 heading.</h5></td>
        </tr>
            <tr>
            <td><code>###### This is a level 6 heading.</code></td>
            <td><code>&lt;h6&gt;This is a level 6 heading.&lt;/h6&gt;</code></td>
            <td><h6>This is a level 6 heading.</h6></td>
        </tr>
    </tbody>
</table>

_The alternate heading syntax, which uses the equals (`=`) and minus (`-`) signs is not supported at the moment._

## Paragraphs

Use a blank line to separate paragraphs.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><pre>This <br>is <br>a <br>paragraph.</pre></td>
            <td><code>&lt;p&gt;This is a paragraph.&lt;/p&gt;</code></td>
            <td><p>This is a paragraph.</p></td>
        </tr>
        <tr>
            <td><pre>This is a paragraph.<br><br>This is another paragraph.</pre></td>
            <td><pre>&lt;p&gt;This is a paragraph.&lt;/p&gt;<br>&lt;p&gt;This is another paragraph.&lt;/p&gt;</pre></td>
            <td><p>This is a paragraph.</p><p>This is another paragraph.</p></td>
        </tr>
    </tbody>
</table>

## Line breaks

End a line with two or more spaces to create a line break (`<br>`).

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><pre>This is a paragraph.  <br>This is still the same paragraph.</pre></td>
            <td><pre>&lt;p&gt;This is a paragraph.&lt;br&gt;<br>This is still the same paragraph.&lt;/p&gt;</pre></td>
            <td><p>This is a paragraph.<br>This is still the same paragraph.</p></td>
        </tr>
    </tbody>
</table>

## Emphasis

Emphasis can be added by making text bold, italic, or both.

### Bold

To make text bold, add two asterisks (`**`) or underscores (`__`) before and after a word, phrase, or letter.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>**This is some bold text.**</code></td>
            <td><code>&lt;p&gt;&lt;strong&gt;This is some bold text.&lt;/strong&gt;&lt;/p&gt;</code></td>
            <td><p><strong>This is some bold text.</strong></p></td>
        </tr>
        <tr>
            <td><code>This is a __bold__ word.</code></td>
            <td><code>&lt;p&gt;This is a &lt;strong&gt;bold&lt;/strong&gt; word.&lt;/p&gt;</code></td>
            <td><p>This is a <strong>bold</strong> word.</p></td>
        </tr>
        <tr>
            <td><code>These are some **b**__o__**l**__d__ letters.</code></td>
            <td><code>&lt;p&gt;These are some &lt;strong&gt;b&lt;/strong&gt;&lt;strong&gt;o&lt;/strong&gt;&lt;strong&gt;l&lt;/strong&gt;&lt;strong&gt;d&lt;/strong&gt; letters.&lt;/p&gt;</code></td>
            <td><p>These are some <strong>b</strong><strong>o</strong><strong>l</strong><strong>d</strong> letters.</p></td>
        </tr>
    </tbody>
</table>

### Italic

To make text italic, add an asterisk (`*`) or underscore (`_`) before and after a word, phrase, or letter.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>*This is some italic text.*</code></td>
            <td><code>&lt;p&gt;&lt;em&gt;This is some italic text.&lt;/em&gt;&lt;/p&gt;</code></td>
            <td><p><em>This is some italic text.</em></p></td>
        </tr>
        <tr>
            <td><code>This is an _italic_ word.</code></td>
            <td><code>&lt;p&gt;This is an &lt;em&gt;italic&lt;/em&gt; word.&lt;/p&gt;</code></td>
            <td><p>This is an <em>italic</em> word.</p></td>
        </tr>
        <tr>
            <td><code>These are some *i*_t_*a*_l_*i*_c_ letters.</code></td>
            <td><code>&lt;p&gt;These are some &lt;em&gt;i&lt;/em&gt;&lt;em&gt;t&lt;/em&gt;&lt;em&gt;a&lt;/em&gt;&lt;em&gt;l&lt;/em&gt;&lt;em&gt;i&lt;/em&gt;&lt;em&gt;c&lt;/em&gt; letters.&lt;/p&gt;</code></td>
            <td><p>These are some <em>i</em><em>t</em><em>a</em><em>l</em><em>i</em><em>c</em> letters.</p></td>
        </tr>
    </tbody>
</table>

### Bold and italic

To make text bold and italic, add three asterisks (`***`) or underscores (`___`) before and after a word, phrase, or letter.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>***This is some bold and italic text.***</code></td>
            <td><code>&lt;p&gt;&lt;em&gt;&lt;strong&gt;This is some bold and italic text.&lt;/strong&gt;&lt;/em&gt;&lt;/p&gt;</code></td>
            <td><p><em><strong>This is some bold and italic text.</strong></em></p></td>
        </tr>
        <tr>
            <td><code>These are some ___bold and italic___ words.</code></td>
            <td><code>&lt;p&gt;These are some &lt;em&gt;&lt;strong&gt;bold and italic&lt;/strong&gt;&lt;/em&gt; words.&lt;/p&gt;</code></td>
            <td><p>These are some <em><strong>bold and italic</strong></em> words.</p></td>
        </tr>
        <tr>
            <td><code>These are some ***b***___o___***l***___d___ ***a***___n___***d*** ___i___***t***___a___***l***___i___***c*** letters.</code></td>
            <td><code>&lt;p&gt;These are some &lt;em&gt;&lt;strong&gt;b&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;o&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;l&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;d&lt;/strong&gt;&lt;/em&gt; &lt;em&gt;&lt;strong&gt;a&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;n&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;d&lt;/strong&gt;&lt;/em&gt; &lt;em&gt;&lt;strong&gt;i&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;t&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;a&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;l&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;i&lt;/strong&gt;&lt;/em&gt;&lt;em&gt;&lt;strong&gt;c&lt;/strong&gt;&lt;/em&gt; letters.&lt;/p&gt;</code></td>
            <td><p>These are some <em><strong>b</strong></em><em><strong>o</strong></em><em><strong>l</strong></em><em><strong>d</strong></em> <em><strong>a</strong></em><em><strong>n</strong></em><em><strong>d</strong></em> <em><strong>i</strong></em><em><strong>t</strong></em><em><strong>a</strong></em><em><strong>l</strong></em><em><strong>i</strong></em><em><strong>c</strong></em> letters.</p></td>
        </tr>
    </tbody>
</table>

## Blockquotes

To create a blockquote, add a number of greater than (`>`) signs before a paragraph. To nest blockquotes, add a number of signs that is greater or lesser than the last one. For example, a level 1 blockquote (`>`) followed by a level 2 blockquote (`>>`).

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
        <tbody>
        <tr>
            <td><code>&gt; This is a level 1 blockquote.</code></td>
            <td><pre>&lt;blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&lt;/blockquote&gt;</pre></td>
            <td><blockquote><p>This is a level 1 blockquote.</p></blockquote></td>
        </tr>
        <tr>
            <td><pre>&gt; This is a level 1 blockquote.<br>&gt; This is another level 1 blockquote.<br>&gt; This is the third level 1 blockquote.</pre></td>
            <td><pre>&lt;blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&lt;p&gt;This is another level 1 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&lt;p&gt;This is the third level 1 blockquote.&lt;/p&gt;<br>&lt;/blockquote&gt;</pre></td>
            <td><blockquote><p>This is a level 1 blockquote.</p><p>This is another level 1 blockquote.</p><p>This is the third level 1 blockquote.</p></blockquote></td>
        </tr>
        <tr>
            <td><pre>&gt;&gt; This is a level 1 blockquote.<br>&gt;&gt; This is a level 2 blockquote.<br>&gt;&gt;&gt; This is a level 3 blockquote.</pre></td>
            <td><pre>&lt;blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&lt;blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 2 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 3 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;/blockquote&gt;<br>&emsp;&emsp;&lt;/blockquote&gt;<br>&lt;/blockquote&gt;</pre></td>
            <td><blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote></blockquote></td>
        </tr>
        <tr>
            <td><pre>&gt; This is a level 1 blockquote.<br>&gt;&gt; This is a level 2 blockquote.<br>&gt;&gt;&gt; This is a level 3 blockquote.<br>&gt;&gt; This is a level 2 blockquote.<br>&gt; This is a level 1 blockquote.</pre></td>
            <td><pre>&lt;blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&lt;blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 2 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 3 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;/blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 2 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&lt;/blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&lt;/blockquote&gt;</pre></td>
            <td><blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote><p>This is a level 2 blockquote.</p></blockquote><p>This is a level 1 blockquote.</p></blockquote></td>
        </tr>
        <tr>
            <td><pre>&gt; This is a level 1 blockquote.<br>&gt;&gt; This is a level 2 blockquote.<br>&gt;&gt;&gt; This is a level 3 blockquote.<br>&gt; This is a level 1 blockquote.</pre></td>
            <td><pre>&lt;blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&lt;blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 2 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;blockquote&gt;<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&lt;p&gt;This is a level 3 blockquote.&lt;/p&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;/blockquote&gt;<br>&emsp;&emsp;&lt;/blockquote&gt;<br>&emsp;&emsp;&lt;p&gt;This is a level 1 blockquote.&lt;/p&gt;<br>&lt;/blockquote&gt;</pre></td>
            <td><blockquote><p>This is a level 1 blockquote.</p><blockquote><p>This is a level 2 blockquote.</p><blockquote><p>This is a level 3 blockquote.</p></blockquote></blockquote><p>This is a level 1 blockquote.</p></blockquote></td>
        </tr>
    </tbody>
</table>

_At the moment, multiline items, such as multiline paragraphs, are not supported inside blockquotes. This means each line is a new item._

## Lists

Items can be organized into ordered and unordered lists.

### Ordered lists

To create an ordered list, add a number, followed by a period (`.`) or closing parenthesis (`)`), followed by a space before a paragraph. The numbers do not have to be in numerical order. To nest ordered lists, add a number of spaces before the number that is greater or lesser than the last number of spaces. For example, a level 1 ordered list (`1. `) followed by a level 2 ordered list. (<code> 1. </code>)

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><pre>1. This is a level 1 ordered list item.<br>2. This is another level 1 ordered list item.<br>3. This is the third level 1 ordered list item.</pre></td>
            <td><pre>&lt;ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 ordered list item.&lt;/li&gt;<br>&lt;/ol&gt;</pre></td>
            <td><ol><li>This is a level 1 ordered list item.</li><li>This is another level 1 ordered list item.</li><li>This is the third level 1 ordered list item.</li></ol></td>
        </tr>
        <tr>
            <td><pre>1) This is a level 1 ordered list item.<br>2) This is another level 1 ordered list item.<br>3) This is the third level 1 ordered list item.</pre></td>
            <td><pre>&lt;ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 ordered list item.&lt;/li&gt;<br>&lt;/ol&gt;</pre></td>
            <td><ol><li>This is a level 1 ordered list item.</li><li>This is another level 1 ordered list item.</li><li>This is the third level 1 ordered list item.</li></ol></td>
        </tr>
        <tr>
            <td><pre>1. This is a level 1 ordered list item.<br>1. This is another level 1 ordered list item.<br>1. This is the third level 1 ordered list item.</pre></td>
            <td><pre>&lt;ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 ordered list item.&lt;/li&gt;<br>&lt;/ol&gt;</pre></td>
            <td><ol><li>This is a level 1 ordered list item.</li><li>This is another level 1 ordered list item.</li><li>This is the third level 1 ordered list item.</li></ol></td>
        </tr>
        <tr>
            <td><pre>82. This is a level 1 ordered list item.<br>6. This is another level 1 ordered list item.<br>14. This is the third level 1 ordered list item.</pre></td>
            <td><pre>&lt;ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 ordered list item.&lt;/li&gt;<br>&lt;/ol&gt;</pre></td>
            <td><ol><li>This is a level 1 ordered list item.</li><li>This is another level 1 ordered list item.</li><li>This is the third level 1 ordered list item.</li></ol></td>
        </tr>
        <tr>
            <td><pre>1. This is a level 1 ordered list item.<br>2. This is another level 1 ordered list item.<br>&emsp;&emsp;1. This is a level 2 ordered list item.<br>&emsp;&emsp;2. This is another level 2 ordered list item.<br>3. This is the third level 1 ordered list item.</pre></td>
            <td><pre>&lt;ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;ol&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is a level 2 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is another level 2 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;/ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 ordered list item.&lt;/li&gt;<br>&lt;/ol&gt;</pre></td>
            <td><ol><li>This is a level 1 ordered list item.</li><li>This is another level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><li>This is another level 2 ordered list item.</li></ol><li>This is the third level 1 ordered list item.</li></ol></td>
        </tr>
        <tr>
            <td><pre>1. This is a level 1 ordered list item.<br>2. This is another level 1 ordered list item.<br>&emsp;&emsp;1. This is a level 2 ordered list item.<br>&emsp;&emsp;&emsp;&emsp;1. This is a level 3 ordered list item.<br>3. This is the third level 1 ordered list item.</pre></td>
            <td><pre>&lt;ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;ol&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is a level 2 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;ol&gt;<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is a level 3 ordered list item.&lt;/li&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;/ol&gt;<br>&emsp;&emsp;&lt;/ol&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 ordered list item.&lt;/li&gt;<br>&lt;/ol&gt;</pre></td>
            <td><ol><li>This is a level 1 ordered list item.</li><li>This is another level 1 ordered list item.</li><ol><li>This is a level 2 ordered list item.</li><ol><li>This is a level 3 ordered list item.</li></ol></ol><li>This is the third level 1 ordered list item.</li></ol></td>
        </tr>
    </tbody>
</table>

### Unordered lists

To create an unordered list, add a dash (`-`), asterisk (`*`), or plus (`+`) sign, followed by a space before a paragraph. To nest unordered lists, add a number of spaces before the dash (`-`), asterisk (`*`), or plus (`+`) sign that is greater or lesser than the last number of spaces. For example, a level 1 unordered list (`- `) followed by a level 2 unordered list. (<code> - </code>)

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><pre>- This is a level 1 unordered list item.<br>- This is another level 1 unordered list item.<br>- This is the third level 1 unordered list item.</pre></td>
            <td><pre>&lt;ul&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 unordered list item.&lt;/li&gt;<br>&lt;/ul&gt;</pre></td>
            <td><ul><li>This is a level 1 unordered list item.</li><li>This is another level 1 unordered list item.</li><li>This is the third level 1 unordered list item.</li></ul></td>
        </tr>
        <tr>
            <td><pre>- This is a level 1 unordered list item.<br>* This is another level 1 unordered list item.<br>+ This is the third level 1 unordered list item.</pre></td>
            <td><pre>&lt;ul&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 unordered list item.&lt;/li&gt;<br>&lt;/ul&gt;</pre></td>
            <td><ul><li>This is a level 1 unordered list item.</li><li>This is another level 1 unordered list item.</li><li>This is the third level 1 unordered list item.</li></ul></td>
        </tr>
        <tr>
            <td><pre>- This is a level 1 unordered list item.<br>- This is another level 1 unordered list item.<br>&emsp;&emsp;- This is a level 2 unordered list item.<br>&emsp;&emsp;- This is another level 2 unordered list item.<br>- This is the third level 1 unordered list item.</pre></td>
            <td><pre>&lt;ul&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;ul&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is a level 2 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is another level 2 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;/ul&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 unordered list item.&lt;/li&gt;<br>&lt;/ul&gt;</pre></td>
            <td><ul><li>This is a level 1 unordered list item.</li><li>This is another level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><li>This is another level 2 unordered list item.</li></ul><li>This is the third level 1 unordered list item.</li></ul></td>
        </tr>
        <tr>
            <td><pre>- This is a level 1 unordered list item.<br>- This is another level 1 unordered list item.<br>&emsp;&emsp;- This is a level 2 unordered list item.<br>&emsp;&emsp;&emsp;&emsp;- This is a level 3 unordered list item.<br>- This is the third level 1 unordered list item.</pre></td>
            <td><pre>&lt;ul&gt;<br>&emsp;&emsp;&lt;li&gt;This is a level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;li&gt;This is another level 1 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&lt;ul&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is a level 2 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;ul&gt;<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&lt;li&gt;This is a level 3 unordered list item.&lt;/li&gt;<br>&emsp;&emsp;&emsp;&emsp;&lt;/ul&gt;<br>&emsp;&emsp;&lt;/ul&gt;<br>&emsp;&emsp;&lt;li&gt;This is the third level 1 unordered list item.&lt;/li&gt;<br>&lt;/ul&gt;</pre></td>
            <td><ul><li>This is a level 1 unordered list item.</li><li>This is another level 1 unordered list item.</li><ul><li>This is a level 2 unordered list item.</li><ul><li>This is a level 3 unordered list item.</li></ul></ul><li>This is the third level 1 unordered list item.</li></ul></td>
        </tr>
    </tbody>
</table>

_At the moment, multiline items, such as multiline paragraphs, are not supported inside lists. This means each line is a new item._

## Code

To denote text as code, add backticks (<code>`</code>) before and after a word or phrase.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>`This is some text denoted as code.`</code></td>
            <td><code>&lt;code&gt;This is some text denoted as code.&lt;/code&gt;</code></td>
            <td><code>This is some text denoted as code.</code></td>
        </tr>
        <tr>
            <td><code>This is a `word` denoted as code.</code></td>
            <td><code>&lt;p&gt;This is a &lt;code&gt;word&lt;/code&gt; denoted as code.&lt;/p&gt;</code></td>
            <td><p>This is a <code>word</code> denoted as code.</p></td>
        </tr>
    </tbody>
</table>

### Escaping backticks

If the word or phrase you want to denote as code includes one or more backticks, you can escape it by using double backticks (<code>``</code>) instead.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>``This is some text denoted as code.``</code></td>
            <td><code>&lt;code&gt;This is some text denoted as code.&lt;/code&gt;</code></td>
            <td><code>This is some text denoted as code.</code></td>
        </tr>
        <tr>
            <td><code>This is a ``word`` denoted as code.</code></td>
            <td><code>&lt;p&gt;This is a &lt;code&gt;word&lt;/code&gt; denoted as code.&lt;/p&gt;</code></td>
            <td><p>This is a <code>word</code> denoted as code.</p></td>
        </tr>
        <tr>
            <td><code>``This code contains `backticks`.``</code></td>
            <td><code>&lt;code&gt;This code contains `backticks`.&lt;/code&gt;</code></td>
            <td><code>This code contains `backticks`.</code></td>
        </tr>
    </tbody>
</table>

_Backticks can also be escaped using a backslash (see [escaping characters](#escaping-characters))_.

## Horizontal Rules

To create a horizontal rule, add three or more asterisks (`***`), minus (`---`) signs, or underscores (`___`) by themselves on a line.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>***</code></td>
            <td><code>&lt;hr&gt;</code></td>
            <td><hr></td>
        </tr>
        <tr>
            <td><code>---</code></td>
            <td><code>&lt;hr&gt;</code></td>
            <td><hr></td>
        </tr>
        <tr>
            <td><code>___</code></td>
            <td><code>&lt;hr&gt;</code></td>
            <td><hr></td>
        </tr>
        <tr>
            <td><code>****</code></td>
            <td><code>&lt;hr&gt;</code></td>
            <td><hr></td>
        </tr>
        <tr>
            <td><code>-----</code></td>
            <td><code>&lt;hr&gt;</code></td>
            <td><hr></td>
        </tr>
        <tr>
            <td><code>______</code></td>
            <td><code>&lt;hr&gt;</code></td>
            <td><hr></td>
        </tr>
    </tbody>
</table>

## Links

To create a link, enclose the link name in square brackets (`[]`), followed by the URL enclosed in parentheses (`()`).

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>[Click me!](https://github.com/ckc-dev/QuickHTML)</code></td>
            <td><code>&lt;a href="https://github.com/ckc-dev/QuickHTML"&gt;Click me!&lt;/a&gt;</code></td>
            <td><a href="https://github.com/ckc-dev/QuickHTML">Click me!</a></td>
        </tr>
        <tr>
            <td><code>Go to [GitHub](https://github.com/)'s main page.</code></td>
            <td><code>&lt;p&gt;Go to &lt;a href="https://github.com/"&gt;GitHub&lt;/a&gt;'s main page.&lt;/p&gt;</code></td>
            <td><p>Go to <a href="https://github.com/">GitHub</a>'s main page.</p></td>
        </tr>
    </tbody>
</table>

### Adding titles to links

A title can optionally be added to a link, it will appear as a tooltip when the link is hovered. To add a title, enclose it in either single (`'`) or double (`"`) quotes after the URL.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>[Click me!](https://github.com/ckc-dev/QuickHTML "Go to the main page of this repository.")</code></td>
            <td><code>&lt;a href="https://github.com/ckc-dev/QuickHTML" title="Go to the main page of this repository."&gt;Click me!&lt;/a&gt;</code></td>
            <td><a href="https://github.com/ckc-dev/QuickHTML" title="Go to the main page of this repository.">Click me!</a></td>
        </tr>
        <tr>
            <td><code>Go to [GitHub](https://github.com/ 'Click here to go to the main page of GitHub.</code></td>
            <td><code>&lt;p&gt;Go to &lt;a href="https://github.com/" title="Click here to go to the main page of GitHub."&gt;GitHub&lt;/a&gt;'s main page.&lt;/p&gt;</code></td>
            <td><p>Go to <a href="https://github.com/" title="Click here to go to the main page of GitHub.">GitHub</a>'s main page.</p></td>
        </tr>
    </tbody>
</table>

## Images

To add an image, use an exclamation mark (`!`), followed by the image `alt` text enclosed in square brackets (`[]`), followed by the image's path or URL enclosed in parentheses (`()`). Titles can be optionally added to images, to add a title, enclose it in either single (`'`) or double (`"`) quotes after the URL.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>![Tux](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png)</code></td>
            <td><code>&lt;img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux"&gt;</code></td>
            <td><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux"></td>
        </tr>
        <tr>
            <td><code>![Tux](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png "lewing@isc.tamu.edu Larry Ewing and The GIMP, CC0, via Wikimedia Commons")</code></td>
            <td><code>&lt;img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux" title="lewing@isc.tamu.edu Larry Ewing and The GIMP, CC0, via Wikimedia Commons"&gt;</code></td>
            <td><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux" title="lewing@isc.tamu.edu Larry Ewing and The GIMP, CC0, via Wikimedia Commons"></td>
        </tr>
    </tbody>
</table>

### Adding links to images

To add a link to an image, enclose the Markdown for the image in square brackets (`[]`), then follow with the link enclosed in parentheses (`()`).

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>[![Tux](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png)](https://commons.wikimedia.org/wiki/File:Tux.svg)</code></td>
            <td><code>&lt;a href="https://commons.wikimedia.org/wiki/File:Tux.svg"&gt;&lt;img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux"&gt;&lt;/a&gt;</code></td>
            <td><a href="https://commons.wikimedia.org/wiki/File:Tux.svg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux"></a></td>
        </tr>
        <tr>
            <td><code>[![Tux](https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png)](https://commons.wikimedia.org/wiki/File:Tux.svg "lewing@isc.tamu.edu Larry Ewing and The GIMP, CC0, via Wikimedia Commons")</code></td>
            <td><code>&lt;a href="https://commons.wikimedia.org/wiki/File:Tux.svg" title="lewing@isc.tamu.edu Larry Ewing and The GIMP, CC0, via Wikimedia Commons"&gt;&lt;img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux"&gt;&lt;/a&gt;</code></td>
            <td><a href="https://commons.wikimedia.org/wiki/File:Tux.svg" title="lewing@isc.tamu.edu Larry Ewing and The GIMP, CC0, via Wikimedia Commons"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/256px-Tux.svg.png" alt="Tux"></a></td>
        </tr>
    </tbody>
</table>

## Escaping characters

Add a backslash (`\`) before a character to escape it, this is often used to display literal characters that would otherwise be used in Markdown syntax.

<table>
    <thead>
        <tr>
            <th>Markdown</th>
            <th>HTML</th>
            <th>Output</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>\# Without the backslash, this would be a heading.</code></td>
            <td><code>&lt;p&gt;# Without the backslash, this would be a heading&lt;/p&gt;</code></td>
            <td><p># Without the backslash, this would be a heading</p></td>
        </tr>
        <tr>
            <td><code>\- Without the backslash, this would be an unordered list item.</code></td>
            <td><code>&lt;p&gt;- Without the backslash, this would be an unordered list item.&lt;/p&gt;</code></td>
            <td><p>- Without the backslash, this would be an unordered list item.</p></td>
        </tr>
    </tbody>
</table>

### Escape sequences

You can use [escape sequences](https://docs.python.org/reference/lexical_analysis.html#literals) when passing strings directly to the `convert()` function.
