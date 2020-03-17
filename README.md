# pathofnoob
Try to ML unique price from POE trade API


Extract mods from poeaffix.net

```javascript
$('div.mod').each(function() {
  line = $(this).find("a").html() + $(this).next("div.VAL:first").find('li').html();
  line = line.replace(/<br>/gi, '@');
  document.writeln(line);
});
```