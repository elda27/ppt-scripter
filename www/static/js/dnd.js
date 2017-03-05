($('document').ready( function() {
  console.log("Ready!");

  function appendFileList(filelist_dom, file)
  {
    filelist_dom.append(
      '<li class="list-group-item"><a class="loadfilename">' + 
      file +
      '</a><div class="notescript"></div></li>'
      ); 
  }

  function putNote(dom, text)
  {
    text.split('\n').forEach(function(paragraph) {
      dom.append('<p class="note">' + paragraph + '</p>')
    });
  }

  function updateNote(filename, text)
  {
    this.filename = filename
    $('.loadfilename').each(function(index, dom) {
      if (dom.innerHTML == this.filename)
      {
        putNote($(dom).parent().children('.notescript'), text)
      }
    }.bind(this));
  }

  function scriptFromJSON(json, filelist_dom)
  {
    if(!(json === undefined))
    {
      filelist_dom.children().remove()
      for(key in json['notes'])
      {
        console.log(key)
        appendFileList(filelist_dom, key)

        updateNote(key, json['notes'][key]);
      }
    }  
  }

  function randomPopinStrings(c) 
  {
    //跳ねさせる要素をすべて取得
    var randomChar = document.getElementsByClassName(c);

    //for で総当たり
    for (var i = 0; i < randomChar.length; i++) {

        //クロージャー
      (function(i) {
          //i 番目の要素、テキスト内容、文字列の長さを取得
          var randomCharI = randomChar[i];
          var randomCharIText = randomCharI.textContent;
          var randomCharLength = randomCharIText.length;
          //何番目の文字を跳ねさせるかをランダムで決める
          var Num = ~~(Math.random() * randomCharLength);

          //跳ねさせる文字を span タグで囲む、それ以外の文字と合わせて再び文字列を作る
          var newRandomChar = randomCharIText.substring(0, Num) + "" + randomCharIText.charAt(Num) + "" + randomCharIText.substring(Num + 1, randomCharLength);
          randomCharI.innerHTML = newRandomChar;

          //アニメーションが終わったら再び関数を発火させる
          span_obj = document.getElementsByClassName(c)[0].children[0]
          if (span_obj === undefined)
          {
            return
          }
          span_obj.addEventListener("animationend", function() {
            randomPopinStrings(c)
            }, false)
          })(i)
        }
      }

  function uploadFiles(files)
  {
    var filelist_dom = $("#filelist");
    filelist_dom.children().remove()
    var fd = new FormData()
    for(file of files)
    {
      appendFileList(filelist_dom, file.name)
      fd.append('fileinputs', file, file.name)
    }

    now_loading_dom = $('.now-loading')
    now_loading_dom.append('Now Uploading...')
    randomPopinStrings('now-loading')

    $.ajax({
      type:'POST',
      contentType: false,
      processData: false,
      url: '/convert',
      data: fd,
      dataType: 'json'
    }).done(
      function(data, textStatus, jqXHR ) {
        console.log('json receive');

        history.pushState(data, null, '/' + data['uuid'])

        $(window).on('popstate', function(event)
        {
          var state = event.originalEvent.state
          console.log(state)
          scriptFromJSON(state, filelist_dom)
          $('.loadfilename').click('click', function()
          {
            $(this).next().slideToggle(300)
          })
        })

        scriptFromJSON(data, filelist_dom)
        
        $('.loadfilename').click('click', function()
        {
          $(this).next().slideToggle(300)
        })

        now_loading_dom = $('.now-loading')
        now_loading_dom.remove()
      });
  }

  var div = $('#drag-drop-area');
  div.on('dragenter', function(event)
  {
    event.stopPropagation()
    event.preventDefault()
    $(this).css('border', '0.3em solid #0B85A1');
  })

  //div.on('dragleave', function(event)
  //{
  //  event.stopPropagation()
  //  event.preventDefault()
  //  $(this).css('border', '0.3em dotted #0B85A1');
  //})

  div.on('dragover', function(event)
  {
    event.stopPropagation()
    event.preventDefault()
  })

  div.on('drop', function(event)
  {
    event.preventDefault()
    $(this).css('border', '0.3em dotted #0B85A1')
    var files = event.originalEvent.dataTransfer.files
    uploadFiles(files)
  })

  $('#file-upload').on('click', function(event) {
    event.preventDefault()
    $('#hidden-file-upload').click()
  })

  $('#hidden-file-upload').change(function(event) {
    console.log('File upload via hidden input')
    event.preventDefault()
    uploadFiles(this.files)
  })

  $('.navigate-help').click(function(event) {
    var n = window.location.href.slice(window.location.href.indexOf('?') + 4)
    var p = $('#help').offset().top
    console.log('Scroll on', p)
    $("html,body").animate({ scrollTop:p }, 'slow')
    return false
  })
}))
