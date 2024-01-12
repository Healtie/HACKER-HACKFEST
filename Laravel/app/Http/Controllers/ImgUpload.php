<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ImgUploadController extends Controller
{
    public function upload(Request $request)
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
        ]);

        $imageName = time().'.'.$request->image->extension();  
   
        $request->image->move(public_path('images'), $imageName);

        $imageUrl = url('images/'.$imageName);

        return response()->json(['url' => $imageUrl], 200);
    }
}
