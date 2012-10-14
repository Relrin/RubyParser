#!/usr/bin/env ruby
# BarcodeGenerator
# uses Gbarcode for encoding barcode data and then rmagick to generate
# images out of it for displaying in views.
# i was using clumsy file.new and file.close for eps generation but
# Adam Feuer had published a much elegant way by using IO.pipe for doing
# same thing.

# this way we can generate any barcode type which Gbarcode -> Gnome Barcode project
# supports.

require 'imagemagick_wrapper'
module ActionView
  class Base
    include ImageMagickWrapper

    id.upcase!
    VALID_BARCODE_OPTIONS = [:encoding_format, :output_format, :width, :height, :scaling_factor, :xoff, :yoff, :margin  ]
   
    def barcode(id, options = {:encoding_format => DEFAULT_ENCODING })
    
      
      options.assert_valid_keys(VALID_BARCODE_OPTIONS)
      output_format = options[:output_format] ? options[:output_format] : DEFAULT_FORMAT
      
      eps = "#{RAILS_ROOT}/public/images/barcodes/#{id}.eps"
      out = "#{RAILS_ROOT}/public/images/barcodes/#{id}.#{output_format}"
     
      #dont generate a barcode again if already generated
      unless File.exists?(out)
        #generate the barcode object with all supplied options
        options[:encoding_format] = DEFAULT_ENCODING unless options[:encoding_format]
        bc = Gbarcode.barcode_create(id)
        bc.width  = options[:width]          if options[:width]
        bc.height = options[:height]         if options[:height]
        bc.scalef = options[:scaling_factor] if options[:scaling_factor]
        bc.xoff   = options[:xoff]           if options[:xoff]
        bc.yoff   = options[:yoff]           if options[:yoff]
        bc.margin = options[:margin]         if options[:margin]
        Gbarcode.barcode_encode(bc, options[:encoding_format])
        
        if options[:no_ascii]
          print_options = Gbarcode::BARCODE_OUT_EPS|Gbarcode::BARCODE_NO_ASCII
        else
          print_options = Gbarcode::BARCODE_OUT_EPS
        end
       
        #encode the barcode object in desired format
        File.open(eps,'wb') do |eps_img|
          Gbarcode.barcode_print(bc, eps_img, print_options)
          eps_img.close
          convert_to_png(eps, out)
        end
        
        #delete the eps image no need to accummulate cruft
        File.delete(eps)
      end
      #send the html image tag
      image_tag("barcodes//#{id}.#{output_format}")
    end   
  end
  
  def helloworld()
    @hello=1
    @c = false
    puts(@hello)
    
    for i in [true, true, false].map{ |p| c || p }
      p i;
    end
    
    k=5
    l=5
    while k<10 && l<10
        k+=1
        l-=1
    end
    
    k=1
    begin
        k+=1
    end while k<15

  end  
end