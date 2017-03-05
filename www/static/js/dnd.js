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
