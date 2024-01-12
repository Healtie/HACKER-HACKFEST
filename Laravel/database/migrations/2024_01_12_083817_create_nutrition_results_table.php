<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('nutrition_results', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('userid');
            $table->float('calories')->nullable();
            $table->float('carbs')->nullable();
            $table->float('fat')->nullable();
            $table->float('protein')->nullable();
            $table->timestamps();
    
            $table->foreign('userid')->references('id')->on('users')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('nutrition_results');
    }
};
